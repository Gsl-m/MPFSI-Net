
import torch




from scipy.io._idl import AttrDict

__C = AttrDict()
cfg = __C


__C.MODEL = AttrDict()
__C.MODEL.BN = 'regularnorm'
__C.MODEL.BNFUNC = torch.nn.BatchNorm2d