# MPFSI-Net

Research implementation for **Multi-attribute semantic localization and support-conditioned local structure modeling for few-shot semantic segmentation**.

## Overview

MPFSI-Net segments a target class in a query image using annotated support images and the target class name. The Multi-Attribute Perception Module (MAPM) produces a spatial prior for each visual attribute description. The Fine-Grained Spatial Interaction Module (FSIM) uses the support representation to guide local feature aggregation in the query image.

## create conda env
```python
conda create -n MPFSI python=3.9
conda activate MPFSI
```

## install packages
```python
pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 -f https://download.pytorch.org/whl/torch_stable.html
pip install opencv-python ftfy regex tqdm ttach tensorboard lxml cython
```



## Data 

- **PASCAL-5i**: Obtain the source images and annotations from [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/).  http://host.robots.ox.ac.uk/pascal/VOC/**COCO-20i**: Obtain the images and annotations from [Microsoft COCO](https://cocodataset.org/).  https://cocodataset.org/

### Usage

- **Stage1** *Pre-training*

  Train the base learner within the standard learning paradigm.

  ```
  sh train_base.sh
  ```

  

- **Stage2** *training*

  Train the meta learner and ensemble module within the meta-learning paradigm.

  ```
  sh train.sh
  ```

  

- **Stage3** *testing*

  Test the proposed model under the standard few-shot setting.

  ```
  sh test.sh
  ```

  
