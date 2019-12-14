#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "dz_s"
__version__ = "0.1.0"
__license__ = "MIT"

import cv2
import sys
import imageio
import face_recognition
import subprocess
from PIL import Image

def get_face_rect(image):
    faces = face_recognition.face_locations(image)
    if len(faces):
        return faces[0]
    else:
        raise Exception('No faces have been detected')

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
 
    image = face_recognition.load_image_file(image_path)
    top, right, bottom, left = get_face_rect(image)
    cropped = image[top:bottom, left:right]
    path = create_gif(cropped)
    #get_optimized_gif(path)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
