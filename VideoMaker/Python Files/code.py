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
shareY = 0
screenLength = 600
iterations = 20

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
    global iterations
    mousePos((-x_pad, -y_pad))
    leftClick()
    for i in range(0, -iterations, -1):
        im = screenGrab()
        findUpArrow(im)
        time.sleep(0.1)

def moreComments(im):
    x = x_pad
    y = screenLength
    #mousePos((x, y))
    if im.getpixel((x, y)) == PixelColour.blackBorder:
        print("########Black Border")
        im1 = ImageOps.grayscale(screenGrab())
        a1 = array(im.getcolors())
        a1 = a1.sum()
    
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -500, 0)
    
        im2 = ImageOps.grayscale(screenGrab())
        a2 = array(im.getcolors())
        a2 = a2.sum()

        # Image has not changed
        if a1 == a2:
            print("Image has not changed")
            mousePos((x, y - 40))
            leftClick()
            time.sleep(10)

            im2 = ImageOps.grayscale(screenGrab())
            a2 = array(im2.getcolors())
            a2 = a2.sum()
            
            if a1 != a2:
                print("More comments loaded")
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -720, 0)
                return True

    return False

def distToTop(y):
    #y = y - y_pad
    return math.floor(y / 100)

def findUpArrow(im):
    global screenLength
    startCord = (Cord.upArrow[0], 0)
    found = False

    # goes down the screen and looking for an arrow
    while not found:
        # pixel colour matches
        if moreComments(im):
            print("The end has been reached")
            break
        
        if im.getpixel(startCord) == PixelColour.upArrow:
            #print("checking pixel")
            # check if the found pixel is part of the arrow
            found = checkImage("upArrow", im, startCord)
            # if not then move down 1 pixel
            if found == False:
                startCord = changeCord(startCord, 0, 1)
        elif startCord[1] < screenLength:
            #print("next pixel")
            startCord = changeCord(startCord, 0, 1)
        else:
            #print("break")
            break
            
    if found == True:
        print("Found arrow!")
        
        # clicks just above the arrow so it can scroll down
        mousePos((startCord[0] - 25, startCord[1] - 15))
        #leftClick()
        # rotations is the amount of times it needs to scroll down
        rotations = distToTop(startCord[1] - 20)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -120 * rotations, 0)

        # the amount of pixels a scroll is
        global scrollDist
        # find the new location of the arrow after scrolling down
        x1 = startCord[0] - 25
        y1 = startCord[1] - 15 - rotations * scrollDist
        
        mousePos((x1, y1))
        time.sleep(0.1)
        # finds where the share button is
        if findShare():
            found = checkImage("upArrow", im, startCord)
            
            # y coordinate of the share button on the screen
            global shareY
            # screenshot parameters for comment
            box = (x1 + x_pad, y1 + y_pad, 965, shareY + 5)
            print("box: ", box)
            if (box[1] < box[3] and found):
                screenshot = ImageGrab.grab(box)
                screenshot.save(os.getcwd() + '\Cropped_Comments' + '\\scshot_' + str(int(time.time())) + '.png', 'PNG')
                # moves down so the arrow can no longer be seen
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -240, 0)
            else:
                print("Cannot take screenshot")
    else:
        #print("Didin't find arrow")
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -240, 0)

def findShare():
    global screenLength
    im = screenGrab()
    startCord = (Cord.shareSide[0], 0)
    found = False
    
    while not found:
        if im.getpixel(startCord) == PixelColour.shareSide:
            print("Checking sharebutton")
            found = checkImage("sharePixel", "null", startCord)
            if found == False:
                startCord = changeCord(startCord, 0, 1)
        elif startCord[1] < screenLength:
            startCord = changeCord(startCord, 0, 1)
        else:
            break
            
    if found == True:
        print("Found share!")
        return True
    else:
        return False
        print("Didn't find share..")

def checkImage(name, im, startCord):
    succ = True
    init = False
    if name == "upArrow":
        for i in range(0, -10, -1):
            if im.getpixel(startCord) == PixelColour.upArrow:
                startCord = changeCord(startCord, 0, -1)
                init = True
            else:
                succ = False
                break

        if succ != False:
            x1 = startCord[0] - 8 + x_pad
            y1 = startCord[1] - 2 + y_pad
            x2 = x1 + 14
            y2 = y1 + 14
            box = (x1, y1, x2, y2)
            #print("box: ", box)
            im = ImageOps.grayscale(ImageGrab.grab(box))
            a = array(im.getcolors())
            a = a.sum()
            #print("arrow gray val", a)
            #im.save(os.getcwd() + '\\ArrowImg__' + str(int(time.time())) +'.png', 'PNG')
            if a == GrayValue.arrow:
                return True
            else:
                return False
            
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
        
        if a == GrayValue.share:
            print("Gray share value match!")
            global shareY

            shareY = y2
            
            return True
        else:
            return False

    if succ == True and init == True:
        print("Check image successful")
        return True
    else:
        return False
        

class PixelColour:
    upArrow = (129, 131, 132)
    #upArrow =(124, 126, 126)
    nameBlueMain = (71, 164, 221)
    shareMain = (26, 26, 27)
    shareSide = (54, 55, 56)
    blackBorder = (3, 3, 3)

class Cord:
    # From Paint.NET
    upArrow = (50 - x_pad, 604 - y_pad) # 11 pixels height of same gradient
    sharePixel = (70 - x_pad, 549 - y_pad)
    shareSide = (69 - x_pad, 549 - y_pad)
    namePixel = (70 - x_pad, 600 - y_pad)

class GrayValue:
    share = 1432
    arrow = 1939
 
if __name__ == '__main__':
    main()
