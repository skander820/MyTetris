#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 11:30
# @Author  : Wu Yingfan
# @Email   : yingfan.w@sunyard.com
# @File    : draw.py
from PIL import Image
import numpy as np
import pygame, time
board=np.ones((3,3))
board[:1,:]=0
print(board)