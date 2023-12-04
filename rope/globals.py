#!/usr/bin/env python3
from typing import List, Optional

mode: Optional[str] = None

source_video_path: Optional[str] = None
target_face_path: Optional[str] = None
export_path: Optional[str] = None

video_quality: Optional[int] = None
threads: Optional[int] = None

gfpgan_enabled: Optional[bool] = None
gfpgan_amount: Optional[int] = None

codeformer_enabled: Optional[bool] = None
codeformer_amount: Optional[int] = None

diffusion_enabled: Optional[bool] = None
diffusion_amount: Optional[int] = None

top_mask_amount: Optional[int] = None
side_mask_amount: Optional[int] = None
bottom_mask_amount: Optional[int] = None
mask_blur: Optional[int] = None

clip_enabled: Optional[bool] = None
clip_text: Optional[str] = None
clip_amount: Optional[int] = None

occluder_enabled: Optional[bool] = None
occluder_amount: Optional[int] = None

faceparser_enabled: Optional[bool] = None
faceparser_amount: Optional[int] = None

blur_amount: Optional[int] = None

threshold_amount: Optional[int] = None

strength: Optional[int] = None

orientation: Optional[int] = None