import math
import os

import torch
from torch import nn
from torch._C import device
import torch.nn.functional as F
from torch.nn import BatchNorm2d as BatchNorm        

import numpy as np
import random
import time
import cv2

import model.resnet as models
import model.vgg as vgg_models
from model.ASPP import ASPP
from model.PPM import PPM
from model.PSPNet import OneModel as PSPNet
# from util.get_mulway_base_data import args
from util.util import get_train_val_set

from model.clip2 import *
from model.get_cam2 import get_img_cam2
# from model.Transformer import Transformer
from pytorch_grad_cam import GradCAM
from model.clip.clip_text import new_class_names, new_class_names_coco, class_text_descriptions, class_text_descriptions_coco
from model.intervolution import Interlooker

def zeroshot_classifier_with_descriptions(classnames, class_text_dict, model):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    with torch.no_grad():
        zeroshot_weights = []

        for classname in classnames:
            texts = class_text_dict[classname]  # 5 条描述文本
            texts = torch.cat((clip.tokenize(texts[0]).to(device), clip.tokenize(texts[1]).to(device), clip.tokenize(texts[2]).to(device), clip.tokenize(texts[3]).to(device), clip.tokenize(texts[4]).to(device)), 0)

            text_embeddings = model.encode_text(texts)
            text_embeddings /= text_embeddings.norm(dim=-1, keepdim=True)

            # 多文本 → 类别原型
            # class_embedding = text_embeddings.mean(dim=0)
            class_embedding = text_embeddings
            class_embedding /= text_embeddings.norm()

            zeroshot_weights.append(class_embedding)

        zeroshot_weights = torch.stack(zeroshot_weights, dim=1).to(device)

    return zeroshot_weights  # [num_classes, text_dim]

def zeroshot_classifier(classnames, templates, model):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    with torch.no_grad():
        zeroshot_weights = []
        for classname in classnames:
            texts = [template.format(classname) for template in templates] #format with class
            texts = clip.tokenize(texts).to(device) #tokenize
            class_embeddings = model.encode_text(texts) #embed with text encoder
            class_embeddings /= class_embeddings.norm(dim=-1, keepdim=True)
            class_embedding = class_embeddings.mean(dim=0)
            class_embedding /= class_embedding.norm()
            zeroshot_weights.append(class_embedding)
        zeroshot_weights = torch.stack(zeroshot_weights, dim=1).to(device)
    return zeroshot_weights.t()

def Weighted_GAP(supp_feat, mask):
    supp_feat = supp_feat * mask
    feat_h, feat_w = supp_feat.shape[-2:][0], supp_feat.shape[-2:][1]
    area = F.avg_pool2d(mask, (supp_feat.size()[2], supp_feat.size()[3])) * feat_h * feat_w + 0.0005
    supp_feat = F.avg_pool2d(input=supp_feat, kernel_size=supp_feat.shape[-2:]) * feat_h * feat_w / area
    return supp_feat

def get_gram_matrix(fea):
    b, c, h, w = fea.shape        
    fea = fea.reshape(b, c, h*w)    # C*N
    fea_T = fea.permute(0, 2, 1)    # N*C
    fea_norm = fea.norm(2, 2, True)
    fea_T_norm = fea_T.norm(2, 1, True)
    gram = torch.bmm(fea, fea_T)/(torch.bmm(fea_norm, fea_T_norm) + 1e-7)    # C*C
    return gram


def reshape_transform(tensor, height=28, width=28):
    tensor = tensor.permute(1, 0, 2)
    result = tensor[:, 1:, :].reshape(tensor.size(0), height, width, tensor.size(2))

    # Bring the channels to the first dimension,
    # like in CNNs.
    result = result.transpose(2, 3).transpose(1, 2)
    return result

class OneModel(nn.Module):
    def __init__(self, args, cls_type=None):
        super(OneModel, self).__init__()

        self.cls_type = cls_type  # 'Base' or 'Novel'
        self.layers = args.layers
        self.zoom_factor = args.zoom_factor
        self.shot = args.shot
        self.vgg = args.vgg
        self.dataset = args.data_set
        self.criterion = nn.CrossEntropyLoss(ignore_index=args.ignore_label)

        self.print_freq = args.print_freq/2

        self.pretrained = True
        self.classes = 2
        if self.dataset == 'pascal':
            self.base_classes = 15
        elif self.dataset == 'coco':
            self.base_classes = 60
        
        assert self.layers in [50, 101, 152]
    
        PSPNet_ = PSPNet(args)
        backbone_str = 'vgg' if args.vgg else 'resnet'+str(args.layers)
        weight_path = 'initmodel/PSPNet/{}/split{}/{}/best.pth'.format(args.data_set, args.split, backbone_str)               
        new_param = torch.load(weight_path, map_location=torch.device('cpu'))['state_dict']
        try: 
            PSPNet_.load_state_dict(new_param)
        except RuntimeError:                   # 1GPU loads mGPU model
            for key in list(new_param.keys()):
                new_param[key[7:]] = new_param.pop(key)
            PSPNet_.load_state_dict(new_param)

        self.layer0, self.layer1, self.layer2, self.layer3, self.layer4 = PSPNet_.layer0, PSPNet_.layer1, PSPNet_.layer2, PSPNet_.layer3, PSPNet_.layer4

        # Base Learner
        self.learner_base = nn.Sequential(PSPNet_.ppm, PSPNet_.cls)

        # Meta Learner
        reduce_dim = 256
        reduce_dim2 = 64
        self.low_fea_id = args.low_fea[-1]
        if self.vgg:
            fea_dim = 512 + 256
        else:
            fea_dim = 1024 + 512           
        self.down_query = nn.Sequential(
            nn.Conv2d(fea_dim, reduce_dim, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=0.5))
        self.down_supp = nn.Sequential(
            nn.Conv2d(fea_dim, reduce_dim, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=0.5))
        mask_add_num = 1
        self.init_merge = nn.Sequential(
            nn.Conv2d(reduce_dim*2 + mask_add_num, reduce_dim, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True))
        self.ASPP_meta = ASPP(reduce_dim2)
        self.res1_meta = nn.Sequential(
            nn.Conv2d(reduce_dim2*5, reduce_dim2, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True))
        self.res2_meta = nn.Sequential(
            nn.Conv2d(reduce_dim2, reduce_dim2, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv2d(reduce_dim2, reduce_dim2, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True))
        self.cls_meta = nn.Sequential(
            nn.Conv2d(reduce_dim2, reduce_dim2, kernel_size=3, padding=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Dropout2d(p=0.1),
            nn.Conv2d(reduce_dim2, self.classes, kernel_size=1))

        # Gram and Meta
        self.gram_merge = nn.Conv2d(2, 1, kernel_size=1, bias=False)
        self.gram_merge.weight = nn.Parameter(torch.tensor([[1.0],[0.0]]).reshape_as(self.gram_merge.weight))

        # Learner Ensemble
        self.cls_merge = nn.Conv2d(2, 1, kernel_size=1, bias=False)
        self.cls_merge.weight = nn.Parameter(torch.tensor([[1.0],[0.0]]).reshape_as(self.cls_merge.weight))

        # K-Shot Reweighting
        if args.shot > 1:
            self.kshot_trans_dim = args.kshot_trans_dim
            if self.kshot_trans_dim == 0:
                self.kshot_rw = nn.Conv2d(self.shot, self.shot, kernel_size=1, bias=False)
                self.kshot_rw.weight = nn.Parameter(torch.ones_like(self.kshot_rw.weight) / args.shot)
            else:
                self.kshot_rw = nn.Sequential(
                    nn.Conv2d(self.shot, self.kshot_trans_dim, kernel_size=1),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(self.kshot_trans_dim, self.shot, kernel_size=1))

        self.sigmoid = nn.Sigmoid()


        # add
        # self.annotation_root = args.annotation_root
        self.clip_model, _ = clip.load(args.clip_path, txt_length=77)
        self.annotation_root = args.annotation_root

        if self.dataset == 'pascal':
            self.bg_text_features = zeroshot_classifier(new_class_names, ['a photo without {}.'],
                                                        self.clip_model)
            self.fg_text_features = zeroshot_classifier_with_descriptions(new_class_names, class_text_descriptions, self.clip_model)
        elif self.dataset == 'coco':
            self.bg_text_features = zeroshot_classifier(new_class_names_coco, ['a photo without {}.'],
                                                        self.clip_model)
            self.fg_text_features = zeroshot_classifier_with_descriptions(new_class_names_coco, class_text_descriptions_coco, self.clip_model)
        #
        # if self.shot == 1:
        #     channel = 523
        # else:
        #     channel = 524
        channel = 523
        self.query_merge = nn.Sequential(
            nn.Conv2d(channel, 64, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True),
        )

        self.supp_merge = nn.Sequential(
            nn.Conv2d(512, 64, kernel_size=1, padding=0, bias=False),
            nn.ReLU(inplace=True),
        )

        # VOLO
        self.invervolution = Interlooker(dim=reduce_dim, out_dim=reduce_dim, kernel_size=3, padding=1, stride=1,
                                         dilation=2, num_heads=1)
        self.text_proj = nn.Linear(2 * reduce_dim, reduce_dim)
        # self.transformer = Transformer(shot=self.shot)

    def get_optim(self, model, args, LR):
        if args.shot > 1:
            optimizer = torch.optim.SGD(
                [     
                {'params': model.down_query.parameters()},
                {'params': model.down_supp.parameters()},
                {'params': model.init_merge.parameters()},
                {'params': model.ASPP_meta.parameters()},
                {'params': model.res1_meta.parameters()},
                {'params': model.res2_meta.parameters()},        
                {'params': model.cls_meta.parameters()},
                {'params': model.query_merge.parameters(),"lr": LR * 10},
                {'params': model.supp_merge.parameters(),"lr": LR * 10},
                {'params': model.invervolution.parameters(), "lr": LR/5},
                {'params': model.gram_merge.parameters()},
                {'params': model.cls_merge.parameters()},
                {'params': model.kshot_rw.parameters()},
                ], lr=LR, momentum=args.momentum, weight_decay=args.weight_decay)
        else:
            optimizer = torch.optim.SGD(
                [     
                {'params': model.down_query.parameters()},
                {'params': model.down_supp.parameters()},
                {'params': model.init_merge.parameters()},
                {'params': model.ASPP_meta.parameters()},
                {'params': model.res1_meta.parameters()},
                {'params': model.res2_meta.parameters()},        
                {'params': model.cls_meta.parameters()},
                {'params': model.query_merge.parameters(), "lr": LR * 10},
                {'params': model.supp_merge.parameters(), "lr": LR * 10},
                {'params': model.invervolution.parameters(), "lr": LR / 5},
                {'params': model.gram_merge.parameters()},
                {'params': model.cls_merge.parameters()},                
                ], lr=LR, momentum=args.momentum, weight_decay=args.weight_decay)
        return optimizer

    def freeze_modules(self, model):
        for param in model.layer0.parameters():
            param.requires_grad = False
        for param in model.layer1.parameters():
            param.requires_grad = False
        for param in model.layer2.parameters():
            param.requires_grad = False
        for param in model.layer3.parameters():
            param.requires_grad = False
        for param in model.layer4.parameters():
            param.requires_grad = False
        for param in model.learner_base.parameters():
            param.requires_grad = False

    def add_clip_feature(self, features, support_mask, cls, text, text_not):
        mask = F.interpolate(support_mask.float(), size=(features.size()[2], features.size()[3]), mode='nearest').long()
        text_feat = self.text_proj(text[cls-1] / text[cls-1].norm(dim=1, keepdim=True)).unsqueeze(2).unsqueeze(2)
        text_feat_not = self.text_proj(text_not[cls-1] / text_not[cls-1].norm(dim=1, keepdim=True)).unsqueeze(2).unsqueeze(2)

        B, _, H, W = mask.size()
        mask_not = mask / 255
        mask_fg = mask - mask_not * 255
        mask_bg = 1 - (mask_not + mask_fg)
        mask_fg = mask_fg.expand(B, 256, H, W) * text_feat
        mask_bg = mask_bg.expand(B, 256, H, W) * text_feat_not
        return features + mask_fg + mask_bg

    # que_img, sup_img, sup_mask, que_mask(meta), que_mask(base), cat_idx(meta)
    def forward(self, x, x_cv2, que_name, class_name, s_x, s_y, cls, text, text_not, cat_idx=None):
        x_size = x.size()
        bs = x_size[0]
        h = int((x_size[2] - 1) / 8 * self.zoom_factor + 1)
        w = int((x_size[3] - 1) / 8 * self.zoom_factor + 1)

        # Query Feature
        with torch.no_grad():
            query_feat_0 = self.layer0(x)
            query_feat_1 = self.layer1(query_feat_0)
            query_feat_2 = self.layer2(query_feat_1)
            query_feat_3 = self.layer3(query_feat_2)
            query_feat_4 = self.layer4(query_feat_3)
            if self.vgg:
                query_feat_2 = F.interpolate(query_feat_2, size=(query_feat_3.size(2),query_feat_3.size(3)), mode='bilinear', align_corners=True)

        query_feat = torch.cat([query_feat_3, query_feat_2], 1)
        query_feat = self.down_query(query_feat)

        # Support Feature
        supp_pro_list = []
        final_supp_list = []
        mask_list = []
        supp_feat_list = []
        supp_feat_list1 = []
        for i in range(self.shot):
            mask = (s_y[:,i,:,:] == 1).float().unsqueeze(1)
            mask_list.append(mask)
            with torch.no_grad():
                supp_feat_0 = self.layer0(s_x[:,i,:,:,:])
                supp_feat_1 = self.layer1(supp_feat_0)
                supp_feat_2 = self.layer2(supp_feat_1)
                supp_feat_3 = self.layer3(supp_feat_2)
                mask = F.interpolate(mask, size=(supp_feat_3.size(2), supp_feat_3.size(3)), mode='bilinear', align_corners=True)
                supp_feat_4 = self.layer4(supp_feat_3*mask)
                final_supp_list.append(supp_feat_4)
                if self.vgg:
                    supp_feat_2 = F.interpolate(supp_feat_2, size=(supp_feat_3.size(2),supp_feat_3.size(3)), mode='bilinear', align_corners=True)
            
            supp_feat = torch.cat([supp_feat_3, supp_feat_2], 1)
            supp_feat = self.down_supp(supp_feat)
            supp_feat_list1.append(supp_feat)
            supp_pro = Weighted_GAP(supp_feat, mask)
            supp_pro_list.append(supp_pro)
            supp_feat_list.append(eval('supp_feat_' + self.low_fea_id))





        # get the vtp
        num_prompts = self.fg_text_features.shape[0]
        img_cam_list_all = []
        for p in range(num_prompts):
            fg_text_feat_p = self.fg_text_features[p]

            target_layers = [self.clip_model.visual.transformer.resblocks[-1].ln_1]
            cam = GradCAM(model=self.clip_model, target_layers=target_layers, reshape_transform=reshape_transform)
            img_cam_list = get_img_cam2(x_cv2, que_name, class_name, self.clip_model, self.bg_text_features, fg_text_feat_p, cam, self.annotation_root, self.training)
            img_cam_list = [F.interpolate(t_img_cam.unsqueeze(0).unsqueeze(0), size=(supp_feat.shape[2], supp_feat.shape[3]),
                          mode='bilinear',
                          align_corners=True) for t_img_cam in img_cam_list]
            img_cam = torch.cat(img_cam_list, 0)
            img_cam = img_cam.repeat(1, 2, 1, 1)
            img_cam_list_all.append(img_cam)


        # K-Shot Reweighting
        que_gram = get_gram_matrix(eval('query_feat_' + self.low_fea_id)) # [bs, C, C] in (0,1)
        norm_max = torch.ones_like(que_gram).norm(dim=(1,2))
        est_val_list = []
        for supp_item in supp_feat_list:
            supp_gram = get_gram_matrix(supp_item)
            gram_diff = que_gram - supp_gram
            est_val_list.append((gram_diff.norm(dim=(1,2))/norm_max).reshape(bs,1,1,1)) # norm2
        est_val_total = torch.cat(est_val_list, 1)  # [bs, shot, 1, 1]
        if self.shot > 1:
            val1, idx1 = est_val_total.sort(1)
            val2, idx2 = idx1.sort(1)
            weight = self.kshot_rw(val1)
            weight = weight.gather(1, idx2)
            weight_soft = torch.softmax(weight, 1)
        else:
            weight_soft = torch.ones_like(est_val_total)
        est_val = (weight_soft * est_val_total).sum(1,True) # [bs, 1, 1, 1]            

        # Prior Similarity Mask
        corr_query_mask_list = []
        cosine_eps = 1e-7
        for i, tmp_supp_feat in enumerate(final_supp_list):
            resize_size = tmp_supp_feat.size(2)
            tmp_mask = F.interpolate(mask_list[i], size=(resize_size, resize_size), mode='bilinear', align_corners=True)

            tmp_supp_feat_4 = tmp_supp_feat * tmp_mask
            q = query_feat_4
            s = tmp_supp_feat_4
            bsize, ch_sz, sp_sz, _ = q.size()[:]

            tmp_query = q
            tmp_query = tmp_query.reshape(bsize, ch_sz, -1)
            tmp_query_norm = torch.norm(tmp_query, 2, 1, True)

            tmp_supp = s               
            tmp_supp = tmp_supp.reshape(bsize, ch_sz, -1) 
            tmp_supp = tmp_supp.permute(0, 2, 1)
            tmp_supp_norm = torch.norm(tmp_supp, 2, 2, True) 

            similarity = torch.bmm(tmp_supp, tmp_query)/(torch.bmm(tmp_supp_norm, tmp_query_norm) + cosine_eps)   
            similarity = similarity.max(1)[0].reshape(bsize, sp_sz*sp_sz)
            similarity = (similarity - similarity.min(1)[0].unsqueeze(1))/(similarity.max(1)[0].unsqueeze(1) - similarity.min(1)[0].unsqueeze(1) + cosine_eps)
            corr_query = similarity.reshape(bsize, 1, sp_sz, sp_sz)
            corr_query = F.interpolate(corr_query, size=(query_feat_3.size()[2], query_feat_3.size()[3]), mode='bilinear', align_corners=True)
            corr_query_mask_list.append(corr_query)
        corr_query_mask = torch.cat(corr_query_mask_list, 1)
        corr_query_mask = (weight_soft * corr_query_mask).sum(1,True)

        # Support Prototype
        supp_pro = torch.cat(supp_pro_list, 2)  # [bs, 256, shot, 1]
        supp_pro = (weight_soft.permute(0,2,1,3) * supp_pro).sum(2,True)

        # Tile & Cat
        concat_feat = supp_pro.expand_as(query_feat)
        # merge_feat = torch.cat([query_feat, concat_feat, corr_query_mask], 1)   # 256+256+1
        # merge_feat = self.init_merge(merge_feat)

        # Base and Meta
        base_out = self.learner_base(query_feat_4)

        # query_meta = self.ASPP_meta(merge_feat)
        # query_meta = self.res1_meta(query_meta)   # 1080->256
        # query_meta = self.res2_meta(query_meta) + query_meta
        # meta_out = self.cls_meta(query_meta)
        volo_feat = self.invervolution(query_feat.permute(0, 2, 3, 1), supp_feat.permute(0, 2, 3, 1))
        volo_feat = self.add_clip_feature(volo_feat.permute(0, 3, 1, 2), s_y, cls, text, text_not)

        # volo_feat0 = self.invervolution(query_feat.permute(0,2,3,1),supp_feat_list1[0].permute(0,2,3,1))
        # volo_feat0 = self.add_clip_feature(volo_feat0.permute(0,3,1,2),torch.unsqueeze(s_y[:,0,:,:], 1),cls,text,text_not)
        #
        # volo_feat1 = self.invervolution(query_feat.permute(0, 2, 3, 1), supp_feat_list1[1].permute(0, 2, 3, 1))
        # volo_feat1 = self.add_clip_feature(volo_feat1.permute(0, 3, 1, 2), torch.unsqueeze(s_y[:, 1, :, :], 1), cls,
        #                                    text, text_not)
        #
        # volo_feat2 = self.invervolution(query_feat.permute(0, 2, 3, 1), supp_feat_list1[2].permute(0, 2, 3, 1))
        # volo_feat2 = self.add_clip_feature(volo_feat2.permute(0, 3, 1, 2), torch.unsqueeze(s_y[:, 2, :, :], 1), cls,
        #                                    text, text_not)
        #
        # volo_feat3 = self.invervolution(query_feat.permute(0, 2, 3, 1), supp_feat_list1[3].permute(0, 2, 3, 1))
        # volo_feat3 = self.add_clip_feature(volo_feat3.permute(0, 3, 1, 2), torch.unsqueeze(s_y[:, 3, :, :], 1), cls,
        #                                    text, text_not)
        #
        # volo_feat4 = self.invervolution(query_feat.permute(0, 2, 3, 1), supp_feat_list1[4].permute(0, 2, 3, 1))
        # volo_feat4 = self.add_clip_feature(volo_feat4.permute(0, 3, 1, 2), torch.unsqueeze(s_y[:, 4, :, :], 1), cls,
        #                                    text, text_not)
        # volo_feat = volo_feat0 + volo_feat1 + volo_feat2 + volo_feat3 + volo_feat4

        if not self.training:
            import matplotlib.pyplot as plt
            if not hasattr(self, 'count'):
                self.count = 0
            vis_save_dir = os.path.join('./saved_cams',f'img_{self.count}')
            os.makedirs(vis_save_dir,exist_ok=True)
            for idx,cam_tensor in enumerate(img_cam_list_all):
                cam_map = cam_tensor[0].detach().cpu()
                if cam_map.dim() == 3:
                    cam_map = cam_map.mean(dim=0)
                cam_map = (cam_map - cam_map.min())/(cam_map.max() - cam_map.min() + 1e-8)
                save_path = os.path.join(vis_save_dir,f'layer_{idx}.png')
                plt.imsave(save_path, cam_map.numpy(), cmap='viridis')
            self.count += 1


        img_cam_all = torch.cat([cam * 2 for cam in img_cam_list_all], dim=1)
        merge_feat = self.query_merge(
            torch.cat([query_feat+volo_feat, concat_feat, img_cam_all, corr_query_mask], dim=1))

        # meta_out, weights = self.transformer(query_feat, supp_feat, mask, img_cam)

        query_meta = self.ASPP_meta(merge_feat)
        query_meta = self.res1_meta(query_meta)   # 1080->256
        query_meta = self.res2_meta(query_meta) + query_meta
        meta_out = self.cls_meta(query_meta)

        meta_out_soft = meta_out.softmax(1)
        base_out_soft = base_out.softmax(1)

        # Classifier Ensemble
        meta_map_bg = meta_out_soft[:,0:1,:,:]                           # [bs, 1, 60, 60]
        meta_map_fg = meta_out_soft[:,1:,:,:]                            # [bs, 1, 60, 60]
        if self.training and self.cls_type == 'Base':
            c_id_array = torch.arange(self.base_classes+1, device='cuda')
            base_map_list = []
            for b_id in range(bs):
                c_id = cat_idx[0][b_id] + 1
                c_mask = (c_id_array!=0)&(c_id_array!=c_id)
                base_map_list.append(base_out_soft[b_id,c_mask,:,:].unsqueeze(0).sum(1,True))
            base_map = torch.cat(base_map_list,0)
            # <alternative implementation>
            # gather_id = (cat_idx[0]+1).reshape(bs,1,1,1).expand_as(base_out_soft[:,0:1,:,:]).cuda()
            # fg_map = base_out_soft.gather(1,gather_id)
            # base_map = base_out_soft[:,1:,:,:].sum(1,True) - fg_map            
        else:
            base_map = base_out_soft[:,1:,:,:].sum(1,True)

        est_map = est_val.expand_as(meta_map_fg)

        meta_map_bg = self.gram_merge(torch.cat([meta_map_bg,est_map], dim=1))
        meta_map_fg = self.gram_merge(torch.cat([meta_map_fg,est_map], dim=1))

        merge_map = torch.cat([meta_map_bg, base_map], 1)
        merge_bg = self.cls_merge(merge_map)                     # [bs, 1, 60, 60]

        final_out = torch.cat([merge_bg, meta_map_fg], dim=1)

        # Output Part
        if self.zoom_factor != 1:
            meta_out = F.interpolate(meta_out, size=(h, w), mode='bilinear', align_corners=True)
            base_out = F.interpolate(base_out, size=(h, w), mode='bilinear', align_corners=True)
            final_out = F.interpolate(final_out, size=(h, w), mode='bilinear', align_corners=True)

        # Loss
        if self.training:
            main_loss = self.criterion(final_out, y_m.long())
            aux_loss1 = self.criterion(meta_out, y_m.long())
            aux_loss2 = self.criterion(base_out, y_b.long())
            return final_out.max(1)[1], main_loss, aux_loss1, aux_loss2
        else:
            return final_out, meta_out, base_out

