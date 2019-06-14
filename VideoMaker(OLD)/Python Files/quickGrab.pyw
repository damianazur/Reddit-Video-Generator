import os, sys, time
import PIL
from PIL import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from numpy import *

x_pad = 26
y_pad = 120

def screenGrab():
    box = (x_pad, y_pad, 987, 727)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

def main():
    screenGrab()
 
if __name__ == '__main__':
    main()
