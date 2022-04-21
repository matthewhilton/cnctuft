import sys
from turtle import color
import numpy as np
import argparse
from PIL import Image, ImageEnhance, ImageTk
import cv2
from tkinter import filedialog
import os
import tkinter
import matplotlib

def quantization(image, clusters=4, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()].reshape((image.shape))

    return res

# Modified from https://github.com/ferretj/pixelate
def pixellize(img, superpixel_size = 4, n_colors = 4):
    saturation = 1.5
    contrast = 1

    img_size = img.size

    # boost saturation of image 
    sat_booster = ImageEnhance.Color(img)
    img = sat_booster.enhance(float(saturation))

    # increase contrast of image
    contr_booster = ImageEnhance.Contrast(img)
    img = contr_booster.enhance(float(contrast))

    # reduce the number of colors used in picture
    img = img.convert('P', palette=Image.ADAPTIVE, colors=n_colors)

    # reduce image size
    superpixel_size = int(superpixel_size)
    reduced_size = (img_size[0] // superpixel_size, img_size[1] // superpixel_size)
    img = img.resize(reduced_size, Image.BICUBIC)

    # resize to original shape to give pixelated look
    img = img.resize(img_size, Image.BICUBIC)

    return img

def process_image(img, pixel_size=4, n_colors=4):
    cv2img  =cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = quantization(cv2img, clusters=7)
    result = Image.fromarray(result[:, :, ::-1].copy())
    pixellized = pixellize(result, pixel_size, n_colors)

    return pixellized

def color_distribution(img):
    # Get the colors in the image
    colorfrequency = img.convert('RGB').getcolors()
    totalpixels = img.height * img.width

    # Package together
    return [(round(color[0] / totalpixels * 100, 2), color[1]) for i, color in enumerate(colorfrequency)]

#### Main UI

filename = "logo.png"
data_save = "data"
img = Image.open(filename)
processed_img = process_image(img) 

print(color_distribution(processed_img))
processed_img.show(processed_img)

# Save image data as numpy array (to not lose any data)
np.save(data_save, np.array(processed_img))