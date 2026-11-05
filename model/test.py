import json
import logging
import os
import pathlib
import re
import numpy as np
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import torch
from model.open_clip.constants import OPENAI_DATASET_MEAN, OPENAI_DATASET_STD
from model.open_clip.model import CLIP, convert_weights_to_lp, convert_to_custom_text_state_dict,\
    resize_pos_embed, get_cast_dtype
from model.open_clip.openai import load_openai_model
from model.open_clip.transform import image_transform
from model.open_clip.tokenizer import tokenize

model_name = 'ViT-L-14'
precision = 'fp32'
device = 'cuda'
model = load_openai_model(
                model_name,
                precision=precision,
                device=device,
        )

print()

