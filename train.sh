#!/bin/sh
PARTITION=Segmentation

GPU_ID=1
dataset=pascal # pascal coco
exp_name=split0

arch=BAM13
net=vgg # vgg resnet50

exp_dir=exp/${dataset}/${arch}/${exp_name}/${net}
snapshot_dir=${exp_dir}/snapshot
result_dir=${exp_dir}/result
config=config/${dataset}/${dataset}_split0_${net}.yaml
#config=config/${dataset}/${dataset}_${split0}_${net}.yaml
mkdir -p ${snapshot_dir} ${result_dir}
now=$(date +"%Y%m%d_%H%M%S")
cp train.sh train.py ${config} ${exp_dir}

echo ${arch}
echo ${config}

# -m torch.distributed.launch --nproc_per_node=4 --master_port=1234
 CUDA_VISIBLE_DEVICES=${GPU_ID} python train.py \
#CUDA_VISIBLE_DEVICES=${GPU_ID} python -m torch.distributed.launch --nproc_per_node=4 --master_port=1234 --use_env train.py \
        --config=${config} \
        --arch=${arch} \
        2>&1 | tee ${resu lt_dir}/train-$now.log
