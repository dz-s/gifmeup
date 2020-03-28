#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "dz_s"
__version__ = "0.1.0"
__license__ = "MIT"

import cv2
import dlib 
import numpy as np
import skimage.draw
import sys
import subprocess

from PIL import Image

def get_face_img(image_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    img = dlib.load_rgb_image(image_path)
    rect = detector(img)[0]
    sp = predictor(img, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])

    outline = landmarks[[*range(17), *range(26,16,-1)]]

    Y, X = skimage.draw.polygon(outline[:,1], outline[:,0])

    cropped_img = np.zeros(img.shape, dtype=np.uint8)
    cropped_img[Y, X] = img[Y, X]
    return cropped_img

def create_frames(image):
    print(image)
    pil_image = Image.fromarray(image)
    frames = []
    for i in range(5):
        frames.append(pil_image.rotate(i*60))
    return frames

def create_gif(image):
    path = 'res.gif'
    frames = create_frames(image)
    frames[0].save(path, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
    return path

def get_optimized_gif(path):
    subprocess.run(['gifsicle', '-O3', path, '-o', 'optimized.gif'], shell=True)

def main():
    """ Main entry point of the app """
    try:
        image_path = sys.argv[1]
    except IndexError as e:
        raise Exception('No path has been provided')
    
    print(image_path)

    cropped = get_face_img(image_path)
    path = create_gif(cropped)
    #get_optimized_gif(path)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
