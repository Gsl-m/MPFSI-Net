
import torch
import torch.nn as nn
import math
import torch.nn.functional as F


class MapMaker(nn.Module):

    def __init__(self,image_size):

        super(MapMaker, self).__init__()
        self.image_size = image_size


    def forward(self, vision_adapter_features,propmt_adapter_features):
        anomaly_maps=[]

        for i,vision_adapter_feature in enumerate(vision_adapter_features):
            B, H, W, C = vision_adapter_feature.shape
            # 将 meta_out 作为掩码进行加权
            # adjusted_feature = vision_adapter_feature * meta_out
            a = vision_adapter_feature.view(B, H * W, C)
            anomaly_map = (vision_adapter_feature.view((B, H * W, C)) @ propmt_adapter_features.float()).contiguous().view(
                (B, H, W, -1)).permute(0, 3, 1, 2)

            anomaly_maps.append(anomaly_map)

        anomaly_map = torch.stack(anomaly_maps, dim=0).mean(dim=0)
        #anomaly_map = F.interpolate(anomaly_map, (81, 81), mode='bilinear', align_corners=True)
        anomaly_map = F.interpolate(anomaly_map, (30,30), mode='bilinear', align_corners=True)
        return torch.softmax(anomaly_map, dim=1)
        # return anomaly_map
