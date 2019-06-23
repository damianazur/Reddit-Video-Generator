import os, sys, time
import PIL
from PIL import Image, ImageGrab, ImageOps
import time, random
from random import randrange
import win32api, win32con
from win32con import *
from numpy import *
import pyperclip

# padding for where the screenshot begins on the screen
x_pad = 26
y_pad = 120
# in pixels how long a scroll is in Chrome
scrollDist = 100
# the y coordinate for the share button
shareY = 0
# how far down does the progream search
screenLength = 600
# how many times it scrolls down after each comment
iterations = 20
# comment number for saving files
commNum = 0
screenShotWidth = 940

# if set to True then commNum counter is set to 0
# files will be overridden
resetCommentNumber = True

# used for virtual key presses
VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A
}

# update the comment number in file
def UpdateCommNum(num):
    f = open("CurrentCommNum" + ".txt", "w")
    f.write(str(num))
    f.close()

# get comment number from file
def getCommNum():
    with open("CurrentCommNum" + ".txt", 'r') as f:
        return f.read()   

# paste the contents from clipboard to a file
def pasteToFile(fileName):
    s = pyperclip.paste() 
    with open(os.getcwd() + '\Text_Files\\' + fileName +'.txt','a+') as g:
        g.write(s + "\n\n")
    g.close()

# Shift + Left Mouse Click
def shiftSelect(*args):
    #print("Shift selecting")
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)

# Used for virtual Ctrl + C
def pressHoldRelease(args):
    '''
    press and hold passed in strings. Once held, release
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').

    this is useful for issuing shortcut command or shift commands.
    e.g. pressHoldRelease('ctrl', 'alt', 'del'), pressHoldRelease('shift','a')
    '''
    for i in args:
        print(i)
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
            
    for i in args:
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
        time.sleep(.1)

def leftClick():
    leftDown()
    leftUp()
    
def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    #print('left release')

def rightDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    #print('right down')
         
def rightUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(.1)
    #print('right release')

# moves mouse to a certain position
def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

# gets coordinates relative to the screenshot range
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x, y)

# takes a screenshot for the range provided
def screenGrab():
    box = (x_pad, y_pad, 987, 727)
    im = ImageGrab.grab(box)
    return im

# used to change the value of tuples because I was confused about something
# and now I can't be bothered changing it because it work
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

# runs at the start
def main():
    # resets or updates the commNum value
    if resetCommentNumber == True:
        UpdateCommNum("0")
    else:
        global commNum
        commNum = int(getCommNum())
        
    global iterations
    # click in the very top left corner of the screen (selects the browser window)
    mousePos((-x_pad, -y_pad))
    leftClick()
    for i in range(0, -iterations, -1):
        im = screenGrab()
        # find the up arrow for each comment
        findUpArrow(im)
        time.sleep(0.1)

# a "load more replies" button appears that needs to be clicked
def moreComments(im):
    x = x_pad
    y = screenLength

    # checks if the black bar at the end is revealed (end of comments)
    if im.getpixel((x, y)) == PixelColour.blackBorder:
        print("Black Border")
        im1 = ImageOps.grayscale(screenGrab())
        a1 = array(im.getcolors())
        a1 = a1.sum()
    
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -500, 0)
    
        im2 = ImageOps.grayscale(screenGrab())
        a2 = array(im.getcolors())
        a2 = a2.sum()

        # Image has not changed
        # Compares the grayscale values
        if a1 == a2:
            print("Image has not changed")
            # click on the load more button
            mousePos((x, y - 40))
            leftClick()
            # wait for comments to appear
            time.sleep(10)

            # get a new screenshot and use it to compare it with the old one
            # to see if the button as been clicked and comments loaded
            im2 = ImageOps.grayscale(screenGrab())
            a2 = array(im2.getcolors())
            a2 = a2.sum()

            # There has been a change
            if a1 != a2:
                print("More comments loaded")
                # scrolls down to prevent the bot from taking down previous comments
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -720, 0)
                return True

    return False

# determines the amount of scrolls down to the comment to reveal as much of
# the content as possible
def distToTop(y):
    return math.floor(y / 100)

# takes a comment and breaks it down into files line by line
# creates line my line screenshots and a line by line .txt file used for balabolka
def sliceComment(srcShot, startY):
    global commNum
    # ImgIndex is the number line in the screenshot
    imgIndex = 1
    # hitText is used for when the bot has reached text and it has to find the
    # cut off point for a screenshot
    hitText = False
    x = 46
    y = 23
    width, height = srcShot.size

    # while not at the end of comment
    while srcShot.getpixel((x, y)) != PixelColour.shareMain and y < height:
        # if reached text
        if srcShot.getpixel((x, y)) != PixelColour.body:
            if hitText == False:
                # click on the start of the line
                mousePos((x - 5, y + startY))
                leftClick()
                # hover over the end of the line and copy it to clipboard
                # then write to file
                mousePos((width, y + startY))
                shiftSelect(("shift"))
                pressHoldRelease(("ctrl", "c"))
                leftClick()
                fileName = '\\comment_' + str(commNum)
                pasteToFile(fileName)

                hitText = True
                
        # if it no longer hovers over text but it used to
        # check if the line can be cut off (screenshot the line and the previous ones)
        elif srcShot.getpixel((x, y)) == PixelColour.body and hitText == True:
            clearLine = True
            for i in range(x, width):
                # there is text in the way so it will move down one pixel and try again
                if srcShot.getpixel((i, y)) != PixelColour.body:
                    clearLine = False
                    break

            # a line not hindered by text has been found, the screenshot is taken and
            # saved to file
            if clearLine == True:
                cropped = srcShot.crop((0, 0, screenShotWidth, y))
                cropped.save(os.getcwd() + '\Cropped_Comments' + '\\comment_' + str(commNum) + '_' + str(imgIndex) + '.png', 'PNG')
                imgIndex += 1
                hitText = False
        
        y += 1

    #if (y >= height):
        #print("Height reached")
    #if (srcShot.getpixel((x, y)) == PixelColour.shareMain):
        #print("Share has been reached")
        
# finds up arrow for comment
def findUpArrow(im):
    global screenLength
    global commNum
    startCord = (Cord.upArrow[0], 0)
    found = False

    # goes down the screen and looking for an arrow
    while not found:
        # pixel colour matches
        if moreComments(im):
            #print("The end has been reached")
            break
        
        if im.getpixel(startCord) == PixelColour.upArrow:
            # check if the found pixel is part of the arrow
            found = checkImage("upArrow", im, startCord)
            # if not then move down 1 pixel
            if found == False:
                startCord = changeCord(startCord, 0, 1)
                
        elif startCord[1] < screenLength:
            startCord = changeCord(startCord, 0, 1)
        else:
            break
            
    if found == True:
        print("Found arrow!")
        
        # clicks just above the arrow so it can scroll down
        mousePos((startCord[0] - 25, startCord[1] - 15))

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
            im = screenGrab()
            found = checkImage("upArrow", im, (startCord[0], startCord[1] - rotations * scrollDist))
            
            # y coordinate of the share button on the screen
            global shareY
            # screenshot parameters for comment
            box = (x1 + x_pad, y1 + y_pad, 965, shareY + 5)
            #print("box: ", box)
            if (box[1] < box[3] and found):
                #print("Saving screenshot")
                screenshot = ImageGrab.grab(box)
                screenshot.save(os.getcwd() + '\Cropped_Comments' + '\\comment_' + str(commNum) + '_0' + '.png', 'PNG')
                sliceComment(screenshot, y1)
                # moves down so the arrow can no longer be seen
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -240, 0)
                # updates the amount of comments
                commNum += 1
                UpdateCommNum(commNum)
                
            else:
                print("---------Cannot take screenshot")
    else:
        #print("Didin't find arrow")
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -240, 0)

# finds the "share" button on the screen (below a comment)
def findShare():
    global screenLength
    # take a new screenshot because scrolling might have been done before
    im = screenGrab()
    startCord = (Cord.shareSide[0], 0)
    found = False
    
    while not found:
        if im.getpixel(startCord) == PixelColour.shareSide:
            #print("Checking sharebutton")
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
        #print("Looking for up arrow")
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
                #print("Arrows Match")
                return True
            else:
                #print("Arrows No Match")
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
        #print("a: ", a)
        
        if a == GrayValue.share:
            #print("Gray share value match!")
            global shareY

            shareY = y2
            
            return True
        else:
            return False

    if succ == True and init == True:
        #print("Check image successful")
        return True
    else:
        return False
        

class PixelColour:
    upArrow = (129, 131, 132)
    nameBlueMain = (71, 164, 221)
    shareMain = (129, 131, 132)
    shareSide = (54, 55, 56)
    blackBorder = (3, 3, 3)
    body = (26, 26, 27)

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


def sliceCommentPic(srcShot):
    imgIndex = 1
    hitText = False
    x = 46
    y = 23
    width, height = srcShot.size

    #mousePos((x, y))
    #time.sleep(3)

    #cropped = srcShot.crop((0, 0, screenShotWidth, 30))
    #cropped.save(os.getcwd() + '\Cropped_Comments' + '\\comment_' + str(commNum) + '_' + str(imgIndex) + '.png', 'PNG')
    
    #print(srcShot.getpixel((x, y)), PixelColour.shareMain)
    while srcShot.getpixel((x, y)) != PixelColour.shareMain and y < height:
        #print("Searching for text")
        if srcShot.getpixel((x, y)) != PixelColour.body:
            if hitText == False:
                print("Text has been hit")
                hitText = True
        elif srcShot.getpixel((x, y)) == PixelColour.body and hitText == True:
            print("Text stopped being hit")
            clearLine = True
            for i in range(x, width):
                #time.sleep(0.01)
                #mousePos((i, y))
                if srcShot.getpixel((i, y)) != PixelColour.body:
                    print("Line broken")
                    clearLine = False
                    break
            
            if clearLine == True:
                print("-Clear line has been found-")
                cropped = srcShot.crop((0, 0, screenShotWidth, y))
                cropped.save(os.getcwd() + '\Cropped_Comments' + '\\comment_' + str(commNum) + '_' + str(imgIndex) + '.png', 'PNG')
                imgIndex += 1
                hitText = False
    
        y += 1

    if (y >= height):
        print("Height reached")
    if (srcShot.getpixel((x, y)) == PixelColour.shareMain):
        print("Share has been reached")
