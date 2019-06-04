import os, sys, time
import PIL
from PIL import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from win32con import *
from numpy import *

x_pad = 26
y_pad = 120
scrollDist = 100

def leftClick():
    leftDown()
    leftUp()

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('left down')
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x, y)

def screenGrab():
    box = (x_pad, y_pad, 987, 727)
    im = ImageGrab.grab(box)
    return im

def changeCord(tup, x, y):
    if x != 0:
        lst = list(tup)
        lst[0] = lst[0] + x
        tup = tuple(lst)

    if y != 0:
        lst = list(tup)
        lst[1] = lst[1] + y
        tup = tuple(lst)
        
    return tup
    
def main():
    im = screenGrab()
    #print("Up arrow colour:", im.getpixel(Cord.upArrow))
    #print("Blue colour:", im.getpixel(Cord.namePixel))
    #mousePos(Cord.namePixel)
    #checkImage("upArrow", im)
    findUpArrow(im)

def distToTop(y):
    #y = y - y_pad
    return math.floor(y / 100)

def findUpArrow(im):
    startCord = (Cord.upArrow[0], 0)
    found = False

    #mousePos(startCord)
    #time.sleep(10)
    
    while not found:
        #mousePos(startCord)
        #time.sleep(0.01)
        #print(startCord[1])
        #print(im.getpixel(startCord))
        if im.getpixel(startCord) == PixelColour.upArrow:
            #print("checking")
            #mousePos(startCord)
            found = checkImage("upArrow", im, startCord)
            if found == False:
                startCord = changeCord(startCord, 0, 1)
        elif startCord[1] < 600:
            startCord = changeCord(startCord, 0, 1)
        else:
            break
            
    if found == True:
        print("Found it!")
        print(distToTop(startCord[1]))
        mousePos((startCord[0], startCord[1] - 20))
        leftClick()
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -120 * distToTop(startCord[1]), 0)
        time.sleep(1)
        findShare()
    else:
        print("Didn't find it..")

def findShare():
    im = screenGrab()
    startCord = (Cord.shareSide[0], 0)
    mousePos(startCord)
    found = False
 
    while not found:
        #mousePos(startCord)
        #time.sleep(0.01)
        #print(startCord[1])
        #print(im.getpixel(startCord))
        if im.getpixel(startCord) == PixelColour.shareSide:
            print("checking sharebutton")
            #mousePos(startCord)
            found = checkImage("sharePixel", "null", startCord)
            if found == False:
                startCord = changeCord(startCord, 0, 1)
        elif startCord[1] < 600:
            startCord = changeCord(startCord, 0, 1)
        else:
            break
            
    if found == True:
        print("Found share!")
    else:
        print("Didn't find share..")

def checkImage(name, im, startCord):
    succ = True
    init = False
    if name == "upArrow":
        #startCord = Cord.upArrow
        for i in range(0, -10, -1):
            #print(i)
            #print(im.getpixel(startCord))
            #print(startCord)
            if im.getpixel(startCord) == PixelColour.upArrow:
                #print("successful")
                startCord = changeCord(startCord, 0, -1)
                init = True
            else:
                #print("fail")
                succ = False
                break
            
    elif name == "sharePixel":
        shareCord = (startCord[0], startCord[1])
        x1 = startCord[0] + x_pad
        y1 = startCord[1] + y_pad - 2
        x2 = x1 + 33
        y2 = y1 + 9
        box = (x1, y1, x2, y2)
        im = ImageOps.grayscale(ImageGrab.grab(box))
        a = array(im.getcolors())
        a = a.sum()
        print("a: ", a)
        im.save(os.getcwd() + '\\seat_one__' + str(int(time.time())) + '.png', 'PNG')
        mousePos(shareCord)
        return True

    if succ == True and init == True:
        print("Very Succ!")
        return True
    else:
        return False
        

class PixelColour:
    upArrow = (129, 131, 132)
    #upArrow =(124, 126, 126)
    nameBlueMain = (71, 164, 221)
    shareMain = (26, 26, 27)
    shareSide = (54, 55, 56)

class Cord:
    # From Paint.NET
    upArrow = (50 - x_pad, 604 - y_pad) # 11 pixels height of same gradient
    sharePixel = (70 - x_pad, 549 - y_pad)
    shareSide = (69 - x_pad, 549 - y_pad)
    namePixel = (70 - x_pad, 600 - y_pad)
 
if __name__ == '__main__':
    main()
