import math
from collections import OrderedDict
from typing import Tuple, Union

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from utils import scoremap2bbox
from typing import Callable, Optional, Sequence, Tuple
from model.open_clip.utils import to_2tuple
from dataclasses import dataclass
from torch.utils.checkpoint import checkpoint
from model.open_clip.transformer import LayerNormFp32, LayerNorm, QuickGELU, Attention, VisionTransformer, TextTransformer

def get_similarity(q, s, mask, attn):
    if len(mask.shape) == 3:
        mask = mask.unsqueeze(1)
    mask = F.interpolate((mask == 1).float(), q.shape[-2:])
    cosine_eps = 1e-7
    s = s * mask
    bsize, ch_sz, sp_sz, _ = q.size()[:]
    tmp_query = q
    tmp_query = tmp_query.contiguous().view(bsize, ch_sz, -1)
    tmp_query_norm = torch.norm(tmp_query, 2, 1, True)
    tmp_supp = s
    tmp_supp = tmp_supp.contiguous().view(bsize, ch_sz, -1).contiguous()
    tmp_supp = tmp_supp.contiguous().permute(0, 2, 1).contiguous()
    tmp_supp_norm = torch.norm(tmp_supp, 2, 2, True)
    similarity = torch.bmm(tmp_supp.float(), tmp_query.float()) / (torch.bmm(tmp_supp_norm.float(), tmp_query_norm.float()) + cosine_eps)
    similarity = similarity.max(1)[0].view(bsize, sp_sz * sp_sz)
    similarity = similarity.view(bsize, 1, sp_sz, sp_sz)


    similarity = similarity[0,0,:,:]
    similarity = similarity.cpu().detach().numpy()

    attn_weight = [aw[:, 1:, 1:] for aw in attn]  # (b, hxw, hxw)
    attn_weight = torch.stack(attn_weight, dim=0)[-8:]  # (8,1,841,841)
    attn_weight = torch.mean(attn_weight, dim=0)  # (1,841,841)
    attn_weight = attn_weight[0].cpu().detach()
    attn_weight = attn_weight.float()

    box, cnt = scoremap2bbox(scoremap=similarity, threshold=0.4, multi_contour_eval=True)
    aff_mask = torch.zeros((similarity.shape[0], similarity.shape[1]))
    for i_ in range(cnt):
        x0_, y0_, x1_, y1_ = box[i_]
        aff_mask[y0_:y1_, x0_:x1_] = 1

    aff_mask = aff_mask.view(1, similarity.shape[0] * similarity.shape[1])  # (1,841)
    aff_mat = attn_weight  # (841,841)

    trans_mat = aff_mat / torch.sum(aff_mat, dim=0, keepdim=True)
    trans_mat = trans_mat / torch.sum(trans_mat, dim=1, keepdim=True)

    for _ in range(2):
        trans_mat = trans_mat / torch.sum(trans_mat, dim=0, keepdim=True)
        trans_mat = trans_mat / torch.sum(trans_mat, dim=1, keepdim=True)
    trans_mat = (trans_mat + trans_mat.transpose(1, 0)) / 2

    for _ in range(1):
        trans_mat = torch.matmul(trans_mat, trans_mat)

    trans_mat = trans_mat * aff_mask

    cam_to_refine = torch.FloatTensor(similarity)
    cam_to_refine = cam_to_refine.view(-1, 1)

    # (n,n) * (n,1)->(n,1)
    # cam_refined = torch.matmul(trans_mat, cam_to_refine).reshape(29,29,1)
    cam_refined = torch.matmul(trans_mat, cam_to_refine)
    cam_refined = cam_refined.reshape(int(math.sqrt(cam_refined.shape[0])), int(math.sqrt(cam_refined.shape[0])), int(cam_refined.shape[1]))
    cam_refined = cam_refined[:,:,0]
    return cam_refined

def upsample_pos_emb(emb, new_size):
    # upsample the pretrained embedding for higher resolution
    # emb size NxD
    first = emb[:1, :]
    emb = emb[1:, :]
    N, D = emb.size(0), emb.size(1)
    size = int(np.sqrt(N))
    assert size * size == N
    #new_size = size * self.upsample
    emb = emb.permute(1, 0)
    emb = emb.view(1, D, size, size).contiguous()
    emb = F.upsample(emb, size=new_size, mode='bilinear',)
    emb = emb.view(D, -1).contiguous()
    emb = emb.permute(1, 0)
    emb = torch.cat([first, emb], 0)
    emb = nn.parameter.Parameter(emb.half())
    return emb

class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1):
        super().__init__()

        # all conv layers have stride 1. an avgpool is performed after the second convolution when stride > 1
        self.conv1 = nn.Conv2d(inplanes, planes, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu1 = nn.ReLU(inplace=True)

        self.conv2 = nn.Conv2d(planes, planes, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.relu2 = nn.ReLU(inplace=True)

        self.avgpool = nn.AvgPool2d(stride) if stride > 1 else nn.Identity()

        self.conv3 = nn.Conv2d(planes, planes * self.expansion, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu3 = nn.ReLU(inplace=True)

        self.downsample = None
        self.stride = stride

        if stride > 1 or inplanes != planes * Bottleneck.expansion:
            # downsampling layer is prepended with an avgpool, and the subsequent convolution has stride 1
            self.downsample = nn.Sequential(OrderedDict([
                ("-1", nn.AvgPool2d(stride)),
                ("0", nn.Conv2d(inplanes, planes * self.expansion, 1, stride=1, bias=False)),
                ("1", nn.BatchNorm2d(planes * self.expansion))
            ]))

    def forward(self, x: torch.Tensor):
        identity = x

        out = self.relu1(self.bn1(self.conv1(x)))
        out = self.relu2(self.bn2(self.conv2(out)))
        out = self.avgpool(out)
        out = self.bn3(self.conv3(out))

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu3(out)
        return out


class AttentionPool2d(nn.Module):
    def __init__(self, spacial_dim: int, embed_dim: int, num_heads: int, output_dim: int = None):
        super().__init__()
        self.positional_embedding = nn.Parameter(torch.randn(spacial_dim ** 2 + 1, embed_dim) / embed_dim ** 0.5)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.c_proj = nn.Linear(embed_dim, output_dim or embed_dim)
        self.num_heads = num_heads

    def forward(self, x, H, W):
        x = x.reshape(x.shape[0], x.shape[1], x.shape[2] * x.shape[3]).permute(2, 0, 1)  # NCHW -> (HW)NC
        x = torch.cat([x.mean(dim=0, keepdim=True), x], dim=0)  # (HW+1)NC
        self.positional_embedding_new = upsample_pos_emb(self.positional_embedding, (H//32,W//32))
        x = x + self.positional_embedding_new[:, None, :].to(x.dtype)  # (HW+1)NC
        x, attn_weight = F.multi_head_attention_forward(
            query=x, key=x, value=x,
            embed_dim_to_check=x.shape[-1],
            num_heads=self.num_heads,
            q_proj_weight=self.q_proj.weight,
            k_proj_weight=self.k_proj.weight,
            v_proj_weight=self.v_proj.weight,
            in_proj_weight=None,
            in_proj_bias=torch.cat([self.q_proj.bias, self.k_proj.bias, self.v_proj.bias]),
            bias_k=None,
            bias_v=None,
            add_zero_attn=False,
            dropout_p=0,
            out_proj_weight=self.c_proj.weight,
            out_proj_bias=self.c_proj.bias,
            use_separate_proj_weight=True,
            training=self.training,
            need_weights=False
        )
        return x[0]


class ModifiedResNet(nn.Module):
    """
    A ResNet class that is similar to torchvision's but contains the following changes:
    - There are now 3 "stem" convolutions as opposed to 1, with an average pool instead of a max pool.
    - Performs anti-aliasing strided convolutions, where an avgpool is prepended to convolutions with stride > 1
    - The final pooling layer is a QKV attention instead of an average pool
    """

    def __init__(self, layers, output_dim, heads, input_resolution=224, width=64):
        super().__init__()
        self.output_dim = output_dim
        self.input_resolution = input_resolution

        # the 3-layer stem
        self.conv1 = nn.Conv2d(3, width // 2, kernel_size=3, stride=2, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(width // 2)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(width // 2, width // 2, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(width // 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(width // 2, width, kernel_size=3, padding=1, bias=False)
        self.bn3 = nn.BatchNorm2d(width)
        self.relu3 = nn.ReLU(inplace=True)
        self.avgpool = nn.AvgPool2d(2)

        # residual layers
        self._inplanes = width  # this is a *mutable* variable used during construction
        self.layer1 = self._make_layer(width, layers[0])
        self.layer2 = self._make_layer(width * 2, layers[1], stride=2)
        self.layer3 = self._make_layer(width * 4, layers[2], stride=2)
        self.layer4 = self._make_layer(width * 8, layers[3], stride=2)

        embed_dim = width * 32  # the ResNet feature dimension
        self.attnpool = AttentionPool2d(input_resolution // 32, embed_dim, heads, output_dim)

    def _make_layer(self, planes, blocks, stride=1):
        layers = [Bottleneck(self._inplanes, planes, stride)]

        self._inplanes = planes * Bottleneck.expansion
        for _ in range(1, blocks):
            layers.append(Bottleneck(self._inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x, H, W):
        def stem(x):
            x = self.relu1(self.bn1(self.conv1(x)))
            x = self.relu2(self.bn2(self.conv2(x)))
            x = self.relu3(self.bn3(self.conv3(x)))
            x = self.avgpool(x)
            return x

        x = x.type(self.conv1.weight.dtype)
        x = stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)#(1,,2048, 7, 7)
        x_pooled = self.attnpool(x, H, W)

        return x_pooled


class LayerNorm(nn.LayerNorm):
    """Subclass torch's LayerNorm to handle fp16."""

    def forward(self, x: torch.Tensor):
        orig_type = x.dtype
        ret = super().forward(x.type(torch.float32))
        return ret.type(orig_type)


class QuickGELU(nn.Module):
    def forward(self, x: torch.Tensor):
        return x * torch.sigmoid(1.702 * x)
class LayerScale(nn.Module):
    def __init__(self, dim, init_values=1e-5, inplace=False):
        super().__init__()
        self.inplace = inplace
        self.gamma = nn.Parameter(init_values * torch.ones(dim))

    def forward(self, x):
        return x.mul_(self.gamma) if self.inplace else x * self.gamma
# class ResidualAttentionBlock(nn.Module):
#     def __init__(
#             self,
#             d_model: int,
#             n_head: int,
#             mlp_ratio: float = 4.0,
#             ls_init_value: float = None,
#             act_layer: Callable = nn.GELU,
#             norm_layer: Callable = LayerNorm,
#             is_cross_attention: bool = False,
#             idx: int = 12,
#     ):
#         super().__init__()
#
#         self.idx = idx
#
#         self.ln_1 = norm_layer(d_model)
#         self.attn = nn.MultiheadAttention(d_model, n_head)
#         self.ls_1 = LayerScale(d_model, ls_init_value) if ls_init_value is not None else nn.Identity()
#         if is_cross_attention:
#             self.ln_1_kv = norm_layer(d_model)
#
#         self.ln_2 = norm_layer(d_model)
#         mlp_width = int(d_model * mlp_ratio)
#         self.mlp = nn.Sequential(OrderedDict([
#             ("c_fc", nn.Linear(d_model, mlp_width)),
#             ("gelu", act_layer()),
#             ("c_proj", nn.Linear(mlp_width, d_model))
#         ]))
#         self.ls_2 = LayerScale(d_model, ls_init_value) if ls_init_value is not None else nn.Identity()
#
#     def attention(
#             self,
#             q_x: torch.Tensor,
#             k_x: Optional[torch.Tensor] = None,
#             v_x: Optional[torch.Tensor] = None,
#             attn_mask: Optional[torch.Tensor] = None,
#     ):
#         k_x = k_x if k_x is not None else q_x
#         v_x = v_x if v_x is not None else q_x
#
#         attn_mask = attn_mask.to(q_x.dtype) if attn_mask is not None else None
#         return self.attn(
#             q_x, k_x, v_x, need_weights=True, attn_mask=attn_mask
#         )
#
#     def forward(
#             self,
#             q_x: torch.Tensor,
#             k_x: Optional[torch.Tensor] = None,
#             v_x: Optional[torch.Tensor] = None,
#             attn_mask: Optional[torch.Tensor] = None,
#     ):
#         k_x = self.ln_1_kv(k_x) if hasattr(self, "ln_1_kv") and k_x is not None else None
#         v_x = self.ln_1_kv(v_x) if hasattr(self, "ln_1_kv") and v_x is not None else None
#
#         tmp, attn = self.attention(q_x=self.ln_1(q_x), k_x=k_x, v_x=v_x, attn_mask=attn_mask)
#         x = q_x + self.ls_1(tmp)
#         x = x + self.ls_2(self.mlp(self.ln_2(x)))
#         return x, attn
class ResidualAttentionBlock(nn.Module):
    def __init__(self, d_model: int, n_head: int, attn_mask: torch.Tensor = None):
        super().__init__()

        self.attn = nn.MultiheadAttention(d_model, n_head)
        self.ln_1 = LayerNorm(d_model)
        self.mlp = nn.Sequential(OrderedDict([
            ("c_fc", nn.Linear(d_model, d_model * 4)),
            ("gelu", QuickGELU()),
            ("c_proj", nn.Linear(d_model * 4, d_model))
        ]))
        self.ln_2 = LayerNorm(d_model)
        self.attn_mask = attn_mask

    def attention(self, x: torch.Tensor):
        self.attn_mask = self.attn_mask.to(dtype=x.dtype, device=x.device) if self.attn_mask is not None else None
        return self.attn(x, x, x, need_weights=True, attn_mask=self.attn_mask)#[0]

    def forward(self, x: torch.Tensor):
        attn_output, attn_weight = self.attention(self.ln_1(x))#(L,N,E)  (N,L,L)
        x = x + attn_output
        x = x + self.mlp(self.ln_2(x))
        return x, attn_weight

# class Transformer(nn.Module):
#     def __init__(
#             self,
#             width: int,
#             layers: int,
#             heads: int,
#             mlp_ratio: float = 4.0,
#             ls_init_value: float = None,
#             act_layer: Callable = nn.GELU,
#             norm_layer: Callable = LayerNorm,
#     ):
#         super().__init__()
#         self.width = width
#         self.layers = layers
#         self.grad_checkpointing = False
#
#         self.resblocks = nn.ModuleList([
#             ResidualAttentionBlock(
#                 width, heads, mlp_ratio, ls_init_value=ls_init_value, act_layer=act_layer, norm_layer=norm_layer,
#                 idx=idx)
#             for idx in range(layers)
#         ])
#
#     def get_cast_dtype(self) -> torch.dtype:
#         return self.resblocks[0].mlp.c_fc.weight.dtype
#
#     def forward(self, x: torch.Tensor, out_layers: list = [],
#                 attn_mask: Optional[torch.Tensor] = None):
#         idx = 0
#         out_attn = []
#         # out_tokens = x
#         out_tokens = []
#         for r in self.resblocks:
#             idx += 1
#             if self.grad_checkpointing and not torch.jit.is_scripting():
#                 # TODO: handle kwargs https://github.com/pytorch/pytorch/issues/79887#issuecomment-1161758372
#                 x = checkpoint(r, x, None, None, attn_mask)
#             else:
#                 if idx == 12:
#                     x, attn = r(x, attn_mask=attn_mask)
#                     out_attn.append(attn)
#                 else:
#                     x, attn_tmp = r(x, attn_mask=attn_mask)
#                 if idx in out_layers:
#                     out_tokens.append(x)
#                     # out_tokens = x
#         return x, out_attn, out_tokens

class Transformer(nn.Module):
    def __init__(self, width: int, layers: int, heads: int, attn_mask: torch.Tensor = None):
        super().__init__()
        self.width = width
        self.layers = layers
        self.resblocks = nn.Sequential(*[ResidualAttentionBlock(width, heads, attn_mask) for _ in range(layers)])

    def forward(self, x: torch.Tensor, out_layers: list = [], extract=None):
        idx = 0
        attn_weights = []
        fts_list = []
        out_tokens = []
        if extract == True:
            with torch.no_grad():
                layers = self.layers
                for i in range(layers):
                    x, attn_weight = self.resblocks[i](x)
                    attn_weights.append(attn_weight)
                    fts_list.append(x)
                x = fts_list
        else:
            with torch.no_grad():
                layers = self.layers if x.shape[0] == 77 else self.layers - 1
                for i in range(layers):
                    idx += 1
                    x, attn_weight = self.resblocks[i](x)
                    attn_weights.append(attn_weight)
                    if idx in out_layers:
                        out_tokens.append(x)

        '''
        for i in range(self.layers-1, self.layers):
            x, attn_weight = self.resblocks[i](x)
            attn_weights.append(attn_weight)
            #feature_map_list.append(x)
        '''
        return x, attn_weights, out_tokens


class VisionTransformer(nn.Module):
    def __init__(self, input_resolution: int, patch_size: int, width: int, layers: int, heads: int, output_dim: int):
        super().__init__()
        self.input_resolution = input_resolution
        self.output_dim = output_dim
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=width, kernel_size=patch_size, stride=patch_size, bias=False)

        scale = width ** -0.5
        self.class_embedding = nn.Parameter(scale * torch.randn(width))
        self.positional_embedding = nn.Parameter(scale * torch.randn((input_resolution // patch_size) ** 2 + 1, width))
        self.ln_pre = LayerNorm(width)

        self.transformer = Transformer(width, layers, heads)

        self.ln_post = LayerNorm(width)
        self.proj = nn.Parameter(scale * torch.randn(width, output_dim))
        self.patch_size = patch_size

    def forward(self, x: torch.Tensor, H, W, outlayers, extract):


        self.positional_embedding_new = upsample_pos_emb(self.positional_embedding, (H//16,W//16))
        x = self.conv1(x)  # shape = [*, width, grid, grid]
        x = x.reshape(x.shape[0], x.shape[1], -1)  # shape = [*, width, grid ** 2]
        x = x.permute(0, 2, 1)  # shape = [*, grid ** 2, width]
        x = torch.cat([self.class_embedding.to(x.dtype) + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device), x], dim=1)  # shape = [*, grid ** 2 + 1, width]
        x = x + self.positional_embedding_new.to(x.dtype)
        x = self.ln_pre(x)

        x = x.permute(1, 0, 2)  # NLD -> LND  #[842,1,768]
        x, attn_weight, out_tokens  = self.transformer(x, outlayers, extract)
        x = x.permute(1, 0, 2)  # LND -> NLD
        out_tokens = [out_tokens[t].permute(1, 0, 2) for t in range(len(out_tokens))]  # LND -> NLD
        '''
        x = x.permute(1, 0, 2)  # LND -> NLD

        x = self.ln_post(x)
        #x = x[:, 0, :]
        #x = x[:,1:,:]
        x = torch.mean(x[:,1:,:],dim=1)
        #feature_map_list.append(x)

        if self.proj is not None:
            x = x @ self.proj
        '''

        return x, attn_weight, out_tokens#cls_attn
# class PatchDropout(nn.Module):
#     """
#     https://arxiv.org/abs/2212.00794
#     """
#
#     def __init__(self, prob, exclude_first_token=True):
#         super().__init__()
#         assert 0 <= prob < 1.
#         self.prob = prob
#         self.exclude_first_token = exclude_first_token  # exclude CLS token
#
#     def forward(self, x):
#         if not self.training or self.prob == 0.:
#             return x
#
#         if self.exclude_first_token:
#             cls_tokens, x = x[:, :1], x[:, 1:]
#         else:
#             cls_tokens = torch.jit.annotate(torch.Tensor, x[:, :1])
#
#         batch = x.size()[0]
#         num_tokens = x.size()[1]
#
#         batch_indices = torch.arange(batch)
#         batch_indices = batch_indices[..., None]
#
#         keep_prob = 1 - self.prob
#         num_patches_keep = max(1, int(num_tokens * keep_prob))
#
#         rand = torch.randn(batch, num_tokens)
#         patch_indices_keep = rand.topk(num_patches_keep, dim=-1).indices
#
#         x = x[batch_indices, patch_indices_keep]
#
#         if self.exclude_first_token:
#             x = torch.cat((cls_tokens, x), dim=1)
#
#         return x
#
# class AttentionalPooler(nn.Module):
#     def __init__(
#             self,
#             d_model: int,
#             context_dim: int,
#             n_head: int = 8,
#             n_queries: int = 256,
#             norm_layer: Callable = LayerNorm
#     ):
#         super().__init__()
#         self.query = nn.Parameter(torch.randn(n_queries, d_model))
#         self.attn = nn.MultiheadAttention(d_model, n_head, kdim=context_dim, vdim=context_dim)
#         self.ln_q = norm_layer(d_model)
#         self.ln_k = norm_layer(context_dim)
#
#     def forward(self, x: torch.Tensor):
#         x = self.ln_k(x).permute(1, 0, 2)  # NLD -> LND
#         N = x.shape[1]
#         q = self.ln_q(self.query)
#         out = self.attn(self._repeat(q, N), x, x, need_weights=False)[0]
#         return out.permute(1, 0, 2)  # LND -> NLD
#
#     def _repeat(self, query, N: int):
#         return query.unsqueeze(1).repeat(1, N, 1)
#
#
# class VisionTransformer(nn.Module):
#     output_tokens: torch.jit.Final[bool]
#
#     def __init__(
#             self,
#             image_size: int,
#             patch_size: int,
#             width: int,
#             layers: int,
#             heads: int,
#             mlp_ratio: float,
#             ls_init_value: float = None,
#             global_average_pool: bool = False,
#             attentional_pool: bool = False,
#             n_queries: int = 256,
#             attn_pooler_heads: int = 8,
#             output_dim: int = 512,
#             patch_dropout: float = 0.,
#             input_patchnorm: bool = False,
#             act_layer: Callable = nn.GELU,
#             norm_layer: Callable = LayerNorm,
#             output_tokens: bool = False
#     ):
#         super().__init__()
#         self.output_tokens = output_tokens
#         image_height, image_width = self.image_size = to_2tuple(image_size)
#         patch_height, patch_width = self.patch_size = to_2tuple(patch_size)
#         self.grid_size = (image_height // patch_height, image_width // patch_width)
#         self.output_dim = output_dim
#
#         # whether to layernorm each patch, as done in dual patchnorm paper - https://arxiv.org/abs/2302.01327v1
#         self.input_patchnorm = input_patchnorm
#
#         if input_patchnorm:
#             patch_input_dim = patch_height * patch_width * 3
#             self.patchnorm_pre_ln = LayerNorm(patch_input_dim)
#             self.conv1 = nn.Linear(patch_input_dim, width)
#         else:
#             self.patchnorm_pre_ln = nn.Identity()
#             self.conv1 = nn.Conv2d(in_channels=3, out_channels=width, kernel_size=patch_size, stride=patch_size,
#                                    bias=False)
#
#         # class embeddings and positional embeddings
#         scale = width ** -0.5
#         self.class_embedding = nn.Parameter(scale * torch.randn(width))
#         self.positional_embedding = nn.Parameter(scale * torch.randn(self.grid_size[0] * self.grid_size[1] + 1, width))
#
#         # setting a patch_dropout of 0. would mean it is disabled and this function would be the identity fn
#         self.patch_dropout = PatchDropout(patch_dropout) if patch_dropout > 0. else nn.Identity()
#
#         self.ln_pre = norm_layer(width)
#         self.transformer = Transformer(
#             width,
#             layers,
#             heads,
#             mlp_ratio,
#             ls_init_value=ls_init_value,
#             act_layer=act_layer,
#             norm_layer=norm_layer,
#         )
#
#
#         self.global_average_pool = global_average_pool
#         if attentional_pool:
#             self.attn_pool = AttentionalPooler(output_dim, width, n_head=attn_pooler_heads, n_queries=n_queries)
#             self.ln_post = norm_layer(output_dim)
#             self.proj = nn.Parameter(scale * torch.randn(output_dim, output_dim))
#         else:
#             self.attn_pool = None
#             self.ln_post = norm_layer(width)
#             self.proj = nn.Parameter(scale * torch.randn(width, output_dim))
#
#
#     def lock(self, unlocked_groups=0, freeze_bn_stats=False):
#         for param in self.parameters():
#             param.requires_grad = False
#
#         if unlocked_groups != 0:
#             groups = [
#                 [
#                     self.conv1,
#                     self.class_embedding,
#                     self.positional_embedding,
#                     self.ln_pre,
#                 ],
#                 *self.transformer.resblocks[:-1],
#                 [
#                     self.transformer.resblocks[-1],
#                     self.ln_post,
#                 ],
#                 self.proj,
#             ]
#
#             def _unlock(x):
#                 if isinstance(x, Sequence):
#                     for g in x:
#                         _unlock(g)
#                 else:
#                     if isinstance(x, torch.nn.Parameter):
#                         x.requires_grad = True
#                     else:
#                         for p in x.parameters():
#                             p.requires_grad = True
#
#             _unlock(groups[-unlocked_groups:])
#
#     @torch.jit.ignore
#     def set_grad_checkpointing(self, enable=True):
#         self.transformer.grad_checkpointing = enable
#
#     def _global_pool(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
#         if self.global_average_pool:
#             return x.mean(dim=1), x
#         else:
#             return x[:, 0], x[:, 1:]
#
#     def forward(self, x: torch.Tensor, out_layers: list):
#
#         # to patches - whether to use dual patchnorm - https://arxiv.org/abs/2302.01327v1
#         if self.input_patchnorm:
#             # einops - rearrange(x, 'b c (h p1) (w p2) -> b (h w) (c p1 p2)')
#             x = x.reshape(x.shape[0], x.shape[1], self.grid_size[0], self.patch_size[0], self.grid_size[1],
#                           self.patch_size[1])
#             x = x.permute(0, 2, 4, 1, 3, 5)
#             x = x.reshape(x.shape[0], self.grid_size[0] * self.grid_size[1], -1)
#             x = self.patchnorm_pre_ln(x)
#             x = self.conv1(x)
#         else:
#             x = self.conv1(x)  # shape = [*, width, grid, grid]
#             x = x.reshape(x.shape[0], x.shape[1], -1)  # shape = [*, width, grid ** 2]
#             x = x.permute(0, 2, 1)  # shape = [*, grid ** 2, width]
#
#         # class embeddings and positional embeddings
#         x = torch.cat(
#             [self.class_embedding.to(x.dtype) + torch.zeros(x.shape[0], 1, x.shape[-1], dtype=x.dtype, device=x.device),
#              x], dim=1)  # shape = [*, grid ** 2 + 1, width]
#         x = x + self.positional_embedding.to(x.dtype)
#
#         x = self.patch_dropout(x)
#         x = self.ln_pre(x)
#
#         x = x.permute(1, 0, 2)  # NLD -> LND
#
#         x, attn, patch_tokens = self.transformer(x, out_layers)
#
#         x = x.permute(1, 0, 2)  # LND -> NLD
#         patch_tokens = [patch_tokens[t].permute(1, 0, 2) for t in range(len(patch_tokens))]  # LND -> NLD
#
#         if self.attn_pool is not None:
#             x = self.attn_pool(x)
#             x = self.ln_post(x)
#             pooled, tokens = self._global_pool(x)
#         else:
#             pooled, tokens = self._global_pool(x)
#             pooled = self.ln_post(pooled)
#
#         if self.proj is not None:
#             pooled = pooled @ self.proj
#
#         if self.output_tokens:
#             return pooled, patch_tokens
#
#         return pooled, patch_tokens
















class CLIP(nn.Module):
    def __init__(self,
                 embed_dim: int,
                 # vision
                 image_resolution: int,
                 vision_layers: Union[Tuple[int, int, int, int], int],
                 vision_width: int,
                 vision_patch_size: int,
                 # text
                 context_length: int,
                 vocab_size: int,
                 transformer_width: int,
                 transformer_heads: int,
                 transformer_layers: int
                 ):
        super().__init__()

        self.context_length = context_length

        if isinstance(vision_layers, (tuple, list)):
            vision_heads = vision_width * 32 // 64
            self.visual = ModifiedResNet(
                layers=vision_layers,
                output_dim=embed_dim,
                heads=vision_heads,
                input_resolution=image_resolution,
                width=vision_width
            )
        else:
            vision_heads = vision_width // 64
            self.visual = VisionTransformer(
                input_resolution=image_resolution,
                patch_size=vision_patch_size,
                width=vision_width,
                layers=vision_layers,
                heads=vision_heads,
                output_dim=embed_dim
            )

        self.transformer = Transformer(
            width=transformer_width,
            layers=transformer_layers,
            heads=transformer_heads,
            attn_mask=self.build_attention_mask()
        )

        self.vocab_size = vocab_size
        self.token_embedding = nn.Embedding(vocab_size, transformer_width)
        self.positional_embedding = nn.Parameter(torch.empty(self.context_length, transformer_width))
        self.ln_final = LayerNorm(transformer_width)

        self.text_projection = nn.Parameter(torch.empty(transformer_width, embed_dim))
        self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))

        self.initialize_parameters()

    def initialize_parameters(self):
        nn.init.normal_(self.token_embedding.weight, std=0.02)
        nn.init.normal_(self.positional_embedding, std=0.01)

        if isinstance(self.visual, ModifiedResNet):
            if self.visual.attnpool is not None:
                std = self.visual.attnpool.c_proj.in_features ** -0.5
                nn.init.normal_(self.visual.attnpool.q_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.k_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.v_proj.weight, std=std)
                nn.init.normal_(self.visual.attnpool.c_proj.weight, std=std)

            for resnet_block in [self.visual.layer1, self.visual.layer2, self.visual.layer3, self.visual.layer4]:
                for name, param in resnet_block.named_parameters():
                    if name.endswith("bn3.weight"):
                        nn.init.zeros_(param)

        proj_std = (self.transformer.width ** -0.5) * ((2 * self.transformer.layers) ** -0.5)
        attn_std = self.transformer.width ** -0.5
        fc_std = (2 * self.transformer.width) ** -0.5
        for block in self.transformer.resblocks:
            nn.init.normal_(block.attn.in_proj_weight, std=attn_std)
            nn.init.normal_(block.attn.out_proj.weight, std=proj_std)
            nn.init.normal_(block.mlp.c_fc.weight, std=fc_std)
            nn.init.normal_(block.mlp.c_proj.weight, std=proj_std)

        if self.text_projection is not None:
            nn.init.normal_(self.text_projection, std=self.transformer.width ** -0.5)

    def build_attention_mask(self):
        # lazily create causal attention mask, with full attention between the vision tokens
        # pytorch uses additive attention mask; fill with -inf
        mask = torch.empty(self.context_length, self.context_length)
        mask.fill_(float("-inf"))
        mask.triu_(1)  # zero out the lower diagonal
        return mask

    @property
    def dtype(self):
        return self.visual.conv1.weight.dtype

    def encode_image(self, image, H, W, outlayers, extract=None):
        return self.visual(image.type(self.dtype), H, W, outlayers, extract)

    def encode_text(self, text):
        x = self.token_embedding(text).type(self.dtype)  # [batch_size, n_ctx, d_model]

        x = x + self.positional_embedding.type(self.dtype)
        x = x.permute(1, 0, 2)  # NLD -> LND
        x, attn_weight, _ = self.transformer(x)
        x = x.permute(1, 0, 2)  # LND -> NLD
        x = self.ln_final(x).type(self.dtype)

        # x.shape = [batch_size, n_ctx, transformer.width]
        # take features from the eot embedding (eot_token is the highest number in each sequence)
        x = x[torch.arange(x.shape[0]), text.argmax(dim=-1)] @ self.text_projection

        return x

    def forward_last_layer(self, image_features, text_features):
        x, attn_weight = self.visual.transformer.resblocks[self.visual.transformer.layers-1](image_features)
        x = x.permute(1, 0, 2)  # LND -> NLD

        x = self.visual.ln_post(x)
        x = torch.mean(x[:, 1:, :], dim=1)

        if self.visual.proj is not None:
            x = x @ self.visual.proj

        image_features = x

        # normalized features
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        text_features = text_features / text_features.norm(dim=1, keepdim=True)
        # cosine similarity as logits
        logit_scale = self.logit_scale.exp()
        logits_per_image = logit_scale * image_features @ text_features.t()

        # shape = [global_batch_size, global_batch_size]
        logits_per_image = logits_per_image.softmax(dim=-1)

        return logits_per_image, attn_weight

    def forward(self, image, text):
        image_features, feature_map, cls_attn = self.encode_image(image)
        with torch.no_grad():
            text_features = self.encode_text(text)

        # normalized features
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        text_features = text_features / text_features.norm(dim=1, keepdim=True)

        # cosine similarity as logits
        logit_scale = self.logit_scale.exp()
        logits_per_image = logit_scale * image_features @ text_features.t()
        #logits_per_text = logits_per_image.t()

        # shape = [global_batch_size, global_batch_size]
        return logits_per_image, logits_per_text
#
# @dataclass
# class CLIPVisionCfg:
#     layers: Union[Tuple[int, int, int, int], int] = 12
#     width: int = 768
#     head_width: int = 64
#     mlp_ratio: float = 4.0
#     patch_size: int = 16
#     image_size: Union[Tuple[int, int], int] = 224
#     ls_init_value: Optional[float] = None  # layer scale initial value
#     patch_dropout: float = 0.  # what fraction of patches to dropout during training (0 would mean disabled and no patches dropped) - 0.5 to 0.75 recommended in the paper for optimal results
#     input_patchnorm: bool = False # whether to use dual patchnorm - would only apply the input layernorm on each patch, as post-layernorm already exist in original clip vit design
#     global_average_pool: bool = False  # whether to global average pool the last embedding layer, instead of using CLS token (https://arxiv.org/abs/2205.01580)
#     attentional_pool: bool = False # whether to use attentional pooler in the last embedding layer
#     n_queries: int = 256 # n_queries for attentional pooler
#     attn_pooler_heads: int = 8 # n heads for attentional_pooling
#     timm_model_name: str = None  # a valid model name overrides layers, width, patch_size
#     timm_model_pretrained: bool = False  # use (imagenet) pretrained weights for named model
#     timm_pool: str = 'avg'  # feature pooling for timm model ('abs_attn', 'rot_attn', 'avg', '')
#     timm_proj: str = 'linear'  # linear projection for timm model output ('linear', 'mlp', '')
#     timm_proj_bias: bool = False  # enable bias final projection
#     timm_drop: float = 0.  # head dropout
#     timm_drop_path: Optional[float] = None  # backbone stochastic depth
#     output_tokens: bool = False
#
# @dataclass
# class CLIPTextCfg:
#     context_length: int = 77
#     vocab_size: int = 49408
#     width: int = 512
#     heads: int = 8
#     layers: int = 12
#     ls_init_value: Optional[float] = None  # layer scale initial value
#     hf_model_name: str = None
#     hf_tokenizer_name: str = None
#     hf_model_pretrained: bool = True
#     proj: str = 'mlp'
#     pooler_type: str = 'mean_pooler'
#     embed_cls: bool = False
#     pad_id: int = 0
#     output_tokens: bool = False
#
#
# def _build_vision_tower(
#         embed_dim: int,
#         vision_cfg: CLIPVisionCfg,
#         quick_gelu: bool = False,
#         cast_dtype: Optional[torch.dtype] = None
# ):
#     if isinstance(vision_cfg, dict):
#         vision_cfg = CLIPVisionCfg(**vision_cfg)
#
#     # OpenAI models are pretrained w/ QuickGELU but native nn.GELU is both faster and more
#     # memory efficient in recent PyTorch releases (>= 1.10).
#     # NOTE: timm models always use native GELU regardless of quick_gelu flag.
#     act_layer = QuickGELU if quick_gelu else nn.GELU
#
#     if isinstance(vision_cfg.layers, (tuple, list)):
#         vision_heads = vision_cfg.width * 32 // vision_cfg.head_width
#         visual = ModifiedResNet(
#             layers=vision_cfg.layers,
#             output_dim=embed_dim,
#             heads=vision_heads,
#             image_size=vision_cfg.image_size,
#             width=vision_cfg.width,
#         )
#     else:
#         vision_heads = vision_cfg.width // vision_cfg.head_width
#         norm_layer = LayerNormFp32 if cast_dtype in (torch.float16, torch.bfloat16) else LayerNorm
#         visual = VisionTransformer(
#             image_size=vision_cfg.image_size,
#             patch_size=vision_cfg.patch_size,
#             width=vision_cfg.width,
#             layers=vision_cfg.layers,
#             heads=vision_heads,
#             mlp_ratio=vision_cfg.mlp_ratio,
#             ls_init_value=vision_cfg.ls_init_value,
#             patch_dropout=vision_cfg.patch_dropout,
#             input_patchnorm=vision_cfg.input_patchnorm,
#             global_average_pool=vision_cfg.global_average_pool,
#             attentional_pool=vision_cfg.attentional_pool,
#             n_queries=vision_cfg.n_queries,
#             attn_pooler_heads=vision_cfg.attn_pooler_heads,
#             output_tokens=vision_cfg.output_tokens,
#             output_dim=embed_dim,
#             act_layer=act_layer,
#             norm_layer=norm_layer,
#         )
#
#     return visual
#
#
# def _build_text_tower(
#         embed_dim: int,
#         text_cfg: CLIPTextCfg,
#         quick_gelu: bool = False,
#         cast_dtype: Optional[torch.dtype] = None,
# ):
#     if isinstance(text_cfg, dict):
#         text_cfg = CLIPTextCfg(**text_cfg)
#
#
#     act_layer = QuickGELU if quick_gelu else nn.GELU
#     norm_layer = LayerNormFp32 if cast_dtype in (torch.float16, torch.bfloat16) else LayerNorm
#
#     text = TextTransformer(
#         context_length=text_cfg.context_length,
#         vocab_size=text_cfg.vocab_size,
#         width=text_cfg.width,
#         heads=text_cfg.heads,
#         layers=text_cfg.layers,
#         ls_init_value=text_cfg.ls_init_value,
#         output_dim=embed_dim,
#         embed_cls=text_cfg.embed_cls,
#         output_tokens=text_cfg.output_tokens,
#         pad_id=text_cfg.pad_id,
#         act_layer=act_layer,
#         norm_layer=norm_layer,
#     )
#
#     return text
#
# class CLIP(nn.Module):
#     output_dict: torch.jit.Final[bool]
#
#     def __init__(
#             self,
#             embed_dim: int,
#             vision_cfg: CLIPVisionCfg,
#             text_cfg: CLIPTextCfg,
#             quick_gelu: bool = False,
#             cast_dtype: Optional[torch.dtype] = None,
#             output_dict: bool = False,
#     ):
#         super().__init__()
#         self.output_dict = output_dict
#         self.visual = _build_vision_tower(embed_dim, vision_cfg, quick_gelu, cast_dtype)
#
#         text = _build_text_tower(embed_dim, text_cfg, quick_gelu, cast_dtype)
#
#         self.transformer = text.transformer
#
#         self.vocab_size = text.vocab_size
#         self.token_embedding = text.token_embedding
#
#         self.positional_embedding = text.positional_embedding
#         self.ln_final = text.ln_final
#         self.text_projection = text.text_projection
#         self.register_buffer('attn_mask', text.attn_mask, persistent=False)
#
#         self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
#
#     def lock_image_tower(self, unlocked_groups=0, freeze_bn_stats=False):
#         self.visual.lock(unlocked_groups=unlocked_groups, freeze_bn_stats=freeze_bn_stats)
#
#     @torch.jit.ignore
#     def set_grad_checkpointing(self, enable=True):
#         self.visual.set_grad_checkpointing(enable)
#         self.transformer.grad_checkpointing = enable
#
#     def encode_image(self, image, out_layers):
#         features = self.visual(image, out_layers)
#         return features
#
#
#     def encode_text(self, text, normalize: bool = False):
#         cast_dtype = self.transformer.get_cast_dtype()
#
#         x = self.token_embedding(text).to(cast_dtype)  # [batch_size, n_ctx, d_model]
#
#         x = x + self.positional_embedding.to(cast_dtype)
#         x = x.permute(1, 0, 2)  # NLD -> LND
#         x, attn, tokens = self.transformer(x, attn_mask=self.attn_mask)
#         x = x.permute(1, 0, 2)  # LND -> NLD
#         x = self.ln_final(x)  # [batch_size, n_ctx, transformer.width]
#         # take features from the eot embedding (eot_token is the highest number in each sequence)
#         x = x[torch.arange(x.shape[0]), text.argmax(dim=-1)] @ self.text_projection
#
#         return F.normalize(x, dim=-1) if normalize else x

def convert_weights(model: nn.Module):
    """Convert applicable model parameters to fp16"""

    def _convert_weights_to_fp16(l):
        if isinstance(l, (nn.Conv1d, nn.Conv2d, nn.Linear)):
            l.weight.data = l.weight.data.half()
            if l.bias is not None:
                l.bias.data = l.bias.data.half()

        if isinstance(l, nn.MultiheadAttention):
            for attr in [*[f"{s}_proj_weight" for s in ["in", "q", "k", "v"]], "in_proj_bias", "bias_k", "bias_v"]:
                tensor = getattr(l, attr)
                if tensor is not None:
                    tensor.data = tensor.data.half()

        for name in ["text_projection", "proj"]:
            if hasattr(l, name):
                attr = getattr(l, name)
                if attr is not None:
                    attr.data = attr.data.half()

    model.apply(_convert_weights_to_fp16)


def build_model(state_dict: dict, txt_length=40):
    vit = "visual.proj" in state_dict
    '''
    inv_freq = 1. / (10000 ** (torch.arange(0, 2048, 2, dtype=torch.float) / 2048))
    position = torch.arange(50, dtype=torch.float)
    sinusoid_inp = torch.einsum('i,j -> ij', position, inv_freq)
    embeddings = torch.cat((sinusoid_inp.sin(), sinusoid_inp.cos()), dim=-1) / 2048 ** 0.5
    state_dict["visual.attnpool.positional_embedding"] = embeddings
    '''
    #state_dict["visual.positional_embedding"] = upsample_pos_emb(state_dict["visual.positional_embedding"], 28)


    if vit:
        vision_width = state_dict["visual.conv1.weight"].shape[0]
        vision_layers = len([k for k in state_dict.keys() if k.startswith("visual.") and k.endswith(".attn.in_proj_weight")])
        vision_patch_size = state_dict["visual.conv1.weight"].shape[-1]
        grid_size = round((state_dict["visual.positional_embedding"].shape[0] - 1) ** 0.5)
        image_resolution = vision_patch_size * grid_size
    else:
        counts: list = [len(set(k.split(".")[2] for k in state_dict if k.startswith(f"visual.layer{b}"))) for b in [1, 2, 3, 4]]
        vision_layers = tuple(counts)
        vision_width = state_dict["visual.layer1.0.conv1.weight"].shape[0]
        output_width = round((state_dict["visual.attnpool.positional_embedding"].shape[0] - 1) ** 0.5)
        vision_patch_size = None
        assert output_width ** 2 + 1 == state_dict["visual.attnpool.positional_embedding"].shape[0]
        image_resolution = output_width * 32

    embed_dim = state_dict["text_projection"].shape[1]
    context_length = state_dict["positional_embedding"].shape[0]
    vocab_size = state_dict["token_embedding.weight"].shape[0]
    transformer_width = state_dict["ln_final.weight"].shape[0]
    transformer_heads = transformer_width // 64
    transformer_layers = len(set(k.split(".")[2] for k in state_dict if k.startswith(f"transformer.resblocks")))

    model = CLIP(
        embed_dim,
        image_resolution, vision_layers, vision_width, vision_patch_size,
        context_length, vocab_size, transformer_width, transformer_heads, transformer_layers
    )

    for key in ["input_resolution", "context_length", "vocab_size"]:
        if key in state_dict:
            del state_dict[key]



    convert_weights(model)
    model.load_state_dict(state_dict, strict=False)
    return model.eval()
# def convert_weights_to_lp(model: nn.Module, dtype=torch.float16):
#     """Convert applicable model parameters to low-precision (bf16 or fp16)"""
#
#     def _convert_weights(l):
#         if isinstance(l, (nn.Conv1d, nn.Conv2d, nn.Linear)):
#             l.weight.data = l.weight.data.to(dtype)
#             if l.bias is not None:
#                 l.bias.data = l.bias.data.to(dtype)
#
#         if isinstance(l, (nn.MultiheadAttention, Attention)):
#             for attr in [*[f"{s}_proj_weight" for s in ["in", "q", "k", "v"]], "in_proj_bias", "bias_k", "bias_v"]:
#                 tensor = getattr(l, attr)
#                 if tensor is not None:
#                     tensor.data = tensor.data.to(dtype)
#
#         for name in ["text_projection", "proj"]:
#             if hasattr(l, name):
#                 attr = getattr(l, name)
#                 if attr is not None:
#                     attr.data = attr.data.to(dtype)
#
#     model.apply(_convert_weights)
#
#
# convert_weights_to_fp16 = convert_weights_to_lp
#
# def build_model(
#         state_dict: dict,
#         quick_gelu=True,
#         cast_dtype=torch.float16,
# ):
#     vit = "visual.proj" in state_dict
#
#     if vit:
#         vision_width = state_dict["visual.conv1.weight"].shape[0]
#         vision_layers = len(
#             [k for k in state_dict.keys() if k.startswith("visual.") and k.endswith(".attn.in_proj_weight")])
#         vision_patch_size = state_dict["visual.conv1.weight"].shape[-1]
#         grid_size = round((state_dict["visual.positional_embedding"].shape[0] - 1) ** 0.5)
#         image_size = vision_patch_size * grid_size
#     else:
#         counts: list = [
#             len(set(k.split(".")[2] for k in state_dict if k.startswith(f"visual.layer{b}"))) for b in [1, 2, 3, 4]]
#         vision_layers = tuple(counts)
#         vision_width = state_dict["visual.layer1.0.conv1.weight"].shape[0]
#         output_width = round((state_dict["visual.attnpool.positional_embedding"].shape[0] - 1) ** 0.5)
#         vision_patch_size = None
#         assert output_width ** 2 + 1 == state_dict["visual.attnpool.positional_embedding"].shape[0]
#         image_size = output_width * 32
#
#     embed_dim = state_dict["text_projection"].shape[1]
#     context_length = state_dict["positional_embedding"].shape[0]
#     vocab_size = state_dict["token_embedding.weight"].shape[0]
#     transformer_width = state_dict["ln_final.weight"].shape[0]
#     transformer_heads = transformer_width // 64
#     transformer_layers = len(set(k.split(".")[2] for k in state_dict if k.startswith(f"transformer.resblocks")))
#
#     vision_cfg = CLIPVisionCfg(
#         layers=vision_layers,
#         width=vision_width,
#         patch_size=vision_patch_size,
#         image_size=image_size,
#     )
#     text_cfg = CLIPTextCfg(
#         context_length=context_length,
#         vocab_size=vocab_size,
#         width=transformer_width,
#         heads=transformer_heads,
#         layers=transformer_layers,
#     )
#
#     model = CLIP(
#         embed_dim,
#         vision_cfg=vision_cfg,
#         text_cfg=text_cfg,
#         quick_gelu=quick_gelu,  # OpenAI models were trained with QuickGELU
#         cast_dtype=cast_dtype,
#     )
#
#     for key in ["input_resolution", "context_length", "vocab_size"]:
#         state_dict.pop(key, None)
#
#     convert_weights_to_fp16(model)  # OpenAI state dicts are partially converted to float16
#     model.load_state_dict(state_dict)
#
#     return model.eval()