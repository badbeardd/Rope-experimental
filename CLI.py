#!/usr/bin/env python3
# Rope EX v24a CLI module
# https://github.com/aquawaves/Rope-experimental
# Original Rope: https://github.com/Hillobar/Rope

import os
import sys
import cv2
from collections import OrderedDict
import numpy as np
from PIL import Image, ImageTk
import json
import time
from skimage import transform as trans
from math import floor, ceil
import copy
import bisect
from platform import system
import argparse
import onnxruntime
import onnx
import torch
from torchvision import transforms
from typing import List

import rope.globals

import rope.Coordinator as Coordinator

from rope.external.clipseg import CLIPDensePredT
from rope.external.insight.face_analysis import FaceAnalysis
import rope.VideoManager as VM

def parse_console_input() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument('-cli', '--console', action=('store_true'), help="Run CLI mode")
    parser.add_argument('-gui', '--graphic', action=('store_true'), help="Run GUI mode")

    parser.add_argument('-s', '--source', type=str, default="", dest='source_video_path', help="Source video path")
    parser.add_argument('-t', '--target', type=str, default="", dest='target_face_path', help="Target face path")
    parser.add_argument('-e', '--output', type=str, default="", dest='export_path', help="Output path")
    parser.add_argument('-vq', '--video_quality', type=int, default="18", dest='video_quality', help="Video quality (1-100) (default: 18)")
    parser.add_argument('-thr', '--threads', type=int, default="2", dest='threads', help="Threads amount (default: 2)")
    parser.add_argument('-tma', '--top_mask_amount', type=int, default="20", dest='top_mask_amount', help="Top mask (default: 20)")
    parser.add_argument('-sma', '--side_mask_amount', type=int, default="20", dest='side_mask_amount', help="Side mask (default: 20)")
    parser.add_argument('-bma', '--bottom_mask_amount', type=int, default="20", dest='bottom_mask_amount', help="Bottom mask (default: 20)")
    parser.add_argument('-msb', '--mask_blur', type=int, default="5", dest='mask_blur', help="Mask blur (default: 5)")
    parser.add_argument('-gfe', '--gfpgan_enabled', action=('store_true'), dest='gfpgan_enabled', help="Enable GFPGAN enhancer")
    parser.add_argument('-gfa', '--gfpgan_amount', type=int, default="100", dest='gfpgan_amount', help="GFPGAN enhancer amount (1-100) (default: 100)")
    parser.add_argument('-cfe', '--codeformer_enabled', action=('store_true'), dest='codeformer_enabled', help="Enable CodeFormer enhancer")
    parser.add_argument('-cfa', '--codeformer_amount', type=int, default="100", dest='codeformer_amount', help="CodeFormer enhancer amount (1-100) (default: 100)")
    parser.add_argument('-dfe', '--diffusion_enabled', action=('store_true'), dest='diffusion_enabled', help="Enable diffusion")
    parser.add_argument('-dfa', '--diffusion_amount', type=int, default="5", dest='diffusion_amount', help="Diffusion amount (1-100) (default: 100)")
    parser.add_argument('-cle', '--clip_enabled', action=('store_true'), dest='clip_enabled', help="Enable CLIP occluder")
    parser.add_argument('-clt', '--clip_text', type=str, default="", dest='clip_text', help="CLIP occluder prompt")
    parser.add_argument('-cla', '--clip_amount', type=int, default="50", dest='clip_amount', help="CLIP occluder amount (1-100) (default: 50)")
    parser.add_argument('-oce', '--occluder_enabled', action=('store_true'), dest='occluder_enabled', help="Enable automatic occluder")
    parser.add_argument('-oca', '--occluder_amount', type=int, default="100", dest='occluder_amount', help="Automatic occluder amount (1-110) (100 is highly recommended) (default: 100)")
    parser.add_argument('-fpe', '--faceparser_enabled', action=('store_true'), dest='faceparser_enabled', help="Enable faceparser")
    parser.add_argument('-fpa', '--faceparser_amount', type=int, default="1", dest='faceparser_amount', help="FaceParser amount (-50-50) (default: 1)")
    parser.add_argument('-bla', '--blur_amount', type=int, default="5", dest='blur_amount', help="Blur amount (default: 5)")
    parser.add_argument('-tha', '--threshold_amount', type=int, default="85", dest='threshold_amount', help="Threshold amount (default: 85)")
    parser.add_argument('-str', '--strength', type=int, default="100", dest='strength', help="Iterations amount (0-500, 100 is one iteration) (default: 100)")
    parser.add_argument('-rtt', '--orientation', type=int, default="0", dest='orientation', help="Target face rotation amount (0-270) (default: 0)")

    args = parser.parse_args()

    if args.console: 
        rope.globals.mode="cli"

    if args.graphic:
        rope.globals.mode="gui"

    rope.globals.source_video_path = args.source_video_path
    rope.globals.target_face_path = args.target_face_path
    rope.globals.export_path = args.export_path
    rope.globals.video_quality = args.video_quality
    rope.globals.threads = args.threads
    rope.globals.top_mask_amount = args.top_mask_amount
    rope.globals.side_mask_amount = args.side_mask_amount
    rope.globals.bottom_mask_amount = args.bottom_mask_amount
    rope.globals.mask_blur = args.mask_blur
    rope.globals.gfpgan_enabled = args.gfpgan_enabled
    rope.globals.gfpgan_amount = args.gfpgan_amount
    rope.globals.codeformer_enabled = args.codeformer_enabled
    rope.globals.codeformer_amount = args.codeformer_amount
    rope.globals.diffusion_enabled = args.diffusion_enabled
    rope.globals.diffusion_amount = args.diffusion_amount
    rope.globals.clip_enabled = args.clip_enabled
    rope.globals.clip_text = args.clip_text
    rope.globals.clip_amount = args.clip_amount
    rope.globals.occluder_enabled = args.occluder_enabled
    rope.globals.occluder_amount = args.occluder_amount
    rope.globals.faceparser_enabled = args.faceparser_enabled
    rope.globals.faceparser_amount = args.faceparser_amount
    rope.globals.blur_amount = args.blur_amount
    rope.globals.threshold_amount = args.threshold_amount
    rope.globals.strength = args.strength
    rope.globals.orientation = args.orientation

    if args.console:
        process()
    elif args.graphic:
        print("Running Rope EX in GUI mode. Please notice that any other startup flags won't work when -gui or --graphic is specified.")
        Coordinator.run()
    elif not args.console and not args.graphic:
        print("You did not provide a startup flag -cli or -gui. Run python3 Rope.py -h to see all available startup flags. Rope EX will stop working now.")
    else:
        print("Unknown exception caught. Rope EX will stop working now.")

def process():
    if rope.globals.source_video_path == None:
        print("No source face path has been specified")
    elif rope.globals.target_face_path == None:
        print("No target video path has been specified")
    elif rope.globals.export_path == None:
        print("No export path has been specified")
    print("Running Rope EX in CLI mode. Please notice that CLI version provides no verbose output while swapping is in progress.")
    Coordinator.load_cli()

def run():
    parse_console_input()

if __name__ == "main":
    run()
