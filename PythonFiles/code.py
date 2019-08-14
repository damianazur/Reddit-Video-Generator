import os, sys, time
import subprocess
import time, random
from random import randrange
from numpy import *
import win32api, win32con
from win32con import *
from win32api import *
import win32com.client
import win32gui
import re

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import shutil
import pyperclip
from pynput.keyboard import Key, Controller
#from moviepy.editor import VideoFileClip

import soundfile as sf
#import pywinauto
#from pywinauto.application import Application
#from pywinauto.keyboard import send_keys

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

thisFilePath = os.getcwd()
os.chdir('..')
repoPath = os.getcwd() + "\\" 
os.chdir(thisFilePath)

chromePath = repoPath + "chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument(f'window-size={1920}x{1080}')

localServerFolder = "TR-Local-Server-Files"

"""
    - Get comments
    - Put comments into an array and then into a dictionary, key being the parent ID
    - Pull comment out one by one
    - With the comment that has been obtained split it into an array of string at every comma or full stop
    - Take the HTML file and input all the info (username, points, time etc)
    - Put the first line of the comment into it
    - Get screenshot of the html file
    - Put in the next line
    - Get next screenshot and repeat the process
"""

import praw
reddit = praw.Reddit(client_id = 'W7V-Goda74pQFA',
                     client_secret = 'H-gI-Ftr8EuSCNliweavIzhnGFM',
                     username = 'AzureScale',
                     password = 'notrandom123',
                     user_agent = 'AzureScale1')

subreddit = reddit.subreddit('AmItheAsshole')

submission3 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c01upz/you_can_fill_a_pool_with_anything_you_want_money/')
submission2 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c193hp/whats_the_most_disturbing_secret_youve_been_told/')
submission1 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c4p6l1/what_happened_at_your_work_which_caused_multiple/')
#hot_python = subreddit.hot(limit = 1)
hot_python = []

startTime = time.time()
commentDict = {}
commentReplies = {}
questionDict = {}
urlEndings = [".com", ".html", ".uk", ".php", ".html", ".org", ".net", ".eu"]
endCharacters = ['.', ',', '?', '!', ')']
otherCharacters = ["“", "”", "\"", "*"]
curseWords = {"fuck" : "f<span style='color: #303030'>&#9608;</span>ck",
              "cunt" : "c<span style='color: #303030'>&#9608;</span>nt",
              "nigger" : "ni<span style='color: #303030'>&#9608;</span>er",
              "shit" : "sh<span style='color: #303030'>&#9608;</span>t",
              "bitch" : "b<span style='color: #303030'>&#9608;</span>tch",
              "dick" : "d<span style='color: #303030'>&#9608;</span>ck",
              " ass " : " as<span style='color: #303030'>&#9608;</span> ",
              "whore" : "wh<span style='color: #303030'>&#9608;</span>re",
              "slut" : "sl<span style='color: #303030'>&#9608;</span>t",
              "pussy" : "pu<span style='color: #303030'>&#9608;</span>sy"}

balabolkaFirstTimeSetup = False
paragraphStyle = 'style="font-size: 20px; LINE-HEIGHT:24px;"'

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
           'z':0x5A,
           'f8':0x77,
           'f4':0x73
}


# get 10,000 ask reddit questions/ subreddits
# put them in a text file
def getTopSubredditPosts():
    top_askreddits = subreddit.top(limit = 10000)
    subredditsTxt = repoPath + "\\SubredditsAITA.txt"
    with open(subredditsTxt,'a+') as g:
        for sub in top_askreddits:
            title = re.sub(r'[^\x00-\x7F]+','\'', sub.title)
            if len(title) < 70:
                g.write(str(sub) + "\t" + title + "\n")           
    g.close()


def leftClick():
    leftDown()
    leftUp()

 
def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)

    
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)


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
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.05)
            
    for i in args:
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
        time.sleep(.1)


def keyPress(args):
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)


def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))


def getComments():
    global questionDict
    neededCharacterCount = commentVideoLength * 15 * 60
    
    for submission in hot_python:
        currentCharacterCount = 0
        if not submission.stickied:
            print(submission)
            print(submission.title, "\n")
            #print(dir(submission))
            #print(submission.selftext)
            global subName
            subName = submission.subreddit
            print("Name:", subName)

            authorName = "deleted"
            if hasattr(submission.author, 'name'):
                authorName = submission.author.name
                
            numComments = formatPoints(submission.num_comments)
            createdTime = formatTime(time.time() - submission.created_utc)
            score = formatPoints(submission.score)
            # put question details into a dictionary
            questionDict[str(submission)] = {"title" : submission.title, "author" : authorName, "numComments" : numComments, "createdTime" : createdTime, "score" : score, "selfText" : submission.selftext}
            #print("submission title: ", questionDict[str(submission)]["title"])

            # I think limit = 0 means that no comment replies are added
            # and limit = 1 would mean only the first level replies (not replies to those replies)
            submission.comments.replace_more(limit = 1)
            commentCount = 0
            # comments in thread
            for comment in submission.comments.list():
                # comment is the first comment
                authorName = "deleted"
                if hasattr(comment.author, 'name'):
                    authorName = comment.author.name
                    
                if comment.parent() == submission and authorName != "AutoModerator":
                    reply = ""
                    replyBody = 0
                    replies = comment.replies
                    if len(replies) != 0:
                        j = 0
                        while j < len(replies) and (replies[j] == "[removed]" or replies[j] == "[deleted]"):
                            j += 1
                        reply = replies[j]
                        replyBody = len(reply.body)

                    # if the amount of characters in the comment is less than 1500 (doesn't spill out of the screen)
                    if len(comment.body) < 1500 and comment.body != "[removed]" and comment.body != "[deleted]":
                        # currentCharacterCount is for the comment and totalCharLength is for that and the replies to it
                        currentCharacterCount += len(comment.body)
                        totalCharLength = len(comment.body) + replyBody
                        
                        # key exists
                        if comment.parent() in commentDict:
                            commentDict[comment.parent()].append(comment)
                        # key does not exist
                        else:
                            commentDict[comment.parent()] = [comment]

                        if totalCharLength < 1400 and replyBody != 0 and reply != "":
                            #print(comment, "has a reply!")
                            commentReplies[str(comment)] = [reply]
                            currentCharacterCount += replyBody

                        commentCount += 1
                        if currentCharacterCount >= neededCharacterCount:
                            #print("Character count reach for getting comments, the needed time has been achieved")
                            break


def printComments():
    for commentArray in commentDict.values():
        for comment in commentArray:
            print(20*'-')
            #print('Parent ID:', comment.parent())
            #print('Comment ID:', comment.id)
            #cleanString(comment.body)
            print(comment.body)


def startDriver():
    global driver
    driver = webdriver.Chrome(executable_path = chromePath, options = chromeOptions)
    driver.get("http://localhost//"+localServerFolder+"//Comments.html")


def captureHTMl(srcNum):
    """
    -- Code for printint the height of a div (Doesn't work as intended but might be useful)
    height = driver.execute_script("return document.body.scrollHeight")
    print(height)
    mainDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "2x-container")))
    print("height:", mainDiv.size["height"])
    """
    driver.execute_script("document.body.style.zoom='200%'")
    driver.save_screenshot(repoPath + 'Videos\\' + threadID + "\\" + commentID + "\\" + srcNum + ".png")


def copyFile():
    shutil.copy2('C://xampp//htdocs//'+localServerFolder+'//Comments_Base.html', 'C://xampp//htdocs//'+localServerFolder+'//Comments.html')


def getSpeakableString(string):
    string = string.replace("<br>", "")
    string = string.replace("*", "")
    string = string.replace("&#x200B;", "")
    string = re.sub(r'[^\x00-\x7F]+','\'', string)
    string = string.strip()

    return string


def splitComment(commentBody):
    global endCharacters
    global otherCharacters
    global urlEndings
    sentences = []
    sIndex = 0
    endIndex = 0
    commentBody = commentBody.replace('\n', '<br>')
    commentBody = commentBody.replace('<br><br><br><br>', '<br><br>')
    commentBody = commentBody.strip() 
    commBodyLen = len(commentBody)

    while endIndex < commBodyLen:
        # skip urls
        if (commentBody[endIndex:endIndex + 6] == "https:" or commentBody[endIndex:endIndex + 5] == "http:") and commentBody[endIndex:endIndex + 4] != "<br>":
            while endIndex < commBodyLen - 1 and commentBody[endIndex] != " " and commentBody[endIndex:endIndex + 4] != "<br>":
                endIndex += 1

        # If the end of a paragrah has been reached
        if endIndex > 7 and commentBody[endIndex - 8:endIndex] == "<br><br>" and commentBody[endIndex -9] not in endCharacters and commentBody[endIndex-9] not in otherCharacters and not commentBody[endIndex-9].isdigit() and commentBody[sIndex:endIndex] != "":
            sentence = commentBody[sIndex:endIndex]
            testSentence = getSpeakableString(sentence)
            if testSentence != "":
                sIndex = endIndex
                #print("$"+sentence+"$")
                sentences.append(sentence)

        # slip comment at certain characters e.g. '.', '?' etc
        if commentBody[endIndex] in endCharacters:
            endIndex += 1
            # keep searching for the character
            while endIndex < commBodyLen and (commentBody[endIndex] in endCharacters or commentBody[endIndex] in otherCharacters or commentBody[endIndex].isdigit()):
                endIndex += 1

            # sometimes there is a fullstop before a digit, we do not split the comment at those points
            if not commentBody[endIndex - 1].isdigit():
                # ignore whitespaces before a <br>
                while endIndex + 5 < commBodyLen - 1 and commentBody[endIndex] == " ":
                    endIndex += 1

                # include all the <br> at the end of the comment piece
                while endIndex + 5 < commBodyLen - 1 and (commentBody[endIndex:endIndex + 4] == "<br>"):
                    endIndex = endIndex + 4

                #print("Appending:", commentBody[sIndex:endIndex])
                sentence = commentBody[sIndex:endIndex]
                # testing is for the audio, some characters are excluded and only a blank line is printed, this is to avoid that
                testSentence = getSpeakableString(sentence)
                if testSentence != "":
                    #print("#"+sentence+"#")
                    sIndex = endIndex
                    sentences.append(sentence)
                    
        endIndex += 1

    if sIndex != endIndex and commentBody[sIndex:endIndex] != "":
        # testing is for the audio, some characters are excluded and only a blank line is printed, this is to avoid that
        testSentence = getSpeakableString(commentBody[sIndex:endIndex])
        if testSentence != "":
            #print("£"+sentence+"£")
            sentence = commentBody[sIndex:endIndex]
            sentences.append(sentence)

    return sentences


def replaceText(newText):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    textDivElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)


def appendDivText(newText):
    global sentenceNum
    global divEnding
    startIndex = 0
    endIndex = 0

    paragraphID = "commentBodyText" + str(sentenceNum) + divEnding
    divID = "commentBodyDiv" + divEnding
    textDivElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, divID)))
    paragraph = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, paragraphID)))
    oldText = paragraph.get_attribute('innerHTML')
    
    while endIndex < len(newText) - 1:
        if newText[endIndex:endIndex + 8] == "<br><br>":
            #print("--Double br found--")
            toAdd = oldText + newText[startIndex:endIndex]
            driver.execute_script("arguments[0].innerHTML = arguments[1];", paragraph, toAdd)
            endIndex += 7
            startIndex = endIndex + 1
            
            sentenceNum += 1
            paragraphID = "commentBodyText" + str(sentenceNum) + divEnding
            #<p class="rz6fp9-10 himKiy" id="commentBodyText1" style="font-size: 20px; LINE-HEIGHT:24px;">
            paragraphTemplate = '<p class="rz6fp9-10 himKiy" id="'+ paragraphID +'" '+ paragraphStyle +'></p>'
            newInnerDiv = textDivElement.get_attribute('innerHTML') + paragraphTemplate
            driver.execute_script("arguments[0].innerHTML = arguments[1];", textDivElement, newInnerDiv)
            paragraph = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, paragraphID)))
            oldText = ""

        endIndex += 1

    if startIndex != endIndex:
        toAdd = oldText + newText[startIndex:endIndex + 1]
        driver.execute_script("arguments[0].innerHTML = arguments[1];", paragraph, toAdd)


def clearCurrentDiv():
    ID = "commentBodyDiv" + divEnding
    paragraphID = "commentBodyText1" + divEnding
    newText = paragraphTemplate = '<p class="rz6fp9-10 himKiy" id="'+ paragraphID +'" '+ paragraphStyle +'></p>'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID)))
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)
    #print(ID, "cleared")

def clearSpecifiedDiv(sDivEnding):
    ID = "commentBodyDiv" + sDivEnding
    paragraphID = "commentBodyText1" + sDivEnding
    newText = paragraphTemplate = '<p class="rz6fp9-10 himKiy" id="'+ paragraphID +'" '+ paragraphStyle +'></p>'
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ID)))
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)

def clearDiv():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDivR")))
    newText = '<p class="rz6fp9-10 himKiy" id="commentBodyText1" '+ paragraphStyle +'></p>'
    newText2 = '<p class="rz6fp9-10 himKiy" id="commentBodyText1R" '+ paragraphStyle +'></p>'
        
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element2, newText2)


def getThreadOpeningVideo():
    global questionDict
    createDir("Title")
    
    usernameBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usernameHere")))
    pointsBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pointsHere")))
    timeBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "timeHere")))
    titleBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "titleHere")))
    commentCountBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentCountHere")))

    driver.execute_script("arguments[0].innerHTML = arguments[1];", usernameBox, questionDict[threadID]["author"])
    driver.execute_script("arguments[0].innerHTML = arguments[1];", pointsBox, questionDict[threadID]["score"])
    driver.execute_script("arguments[0].innerHTML = arguments[1];", timeBox, questionDict[threadID]["createdTime"])
    driver.execute_script("arguments[0].innerHTML = arguments[1];", titleBox, questionDict[threadID]["title"])
    driver.execute_script("arguments[0].innerHTML = arguments[1];", commentCountBox, questionDict[threadID]["numComments"])
    
    driver.execute_script("document.body.style.zoom='200%'")
    divVis("commentFooter", "none")
    time.sleep(0.5)
    driver.save_screenshot(repoPath + 'Videos\\' + threadID + "\\Title\\1.png")

    global commentID
    commentID = "Title"
    writeToFile("title", questionDict[threadID]["title"])

    global subName
    global sentenceNum
    if subName == "AmItheAsshole":
        #print("getThreadOpeningVideo:", subName)
        global divEnding
        divEnding = ""
        
        # image counter is used for saving as a screenshot
        imageCounter = 2
        
        commentBody = questionDict[threadID]["selfText"]
        comment = splitComment(commentBody)
        commentLen = len(comment)

        # index is used for displaying the footer when the comment is coming to an end
        index = 1
        # sentenceNum is used for the paragraph index when writing to the HTML file
        sentenceNum = 1
        # Iterate over every comment piece
        for commentPiece in comment:
            # write to file
            writeToFile("title", commentPiece)
                        
            # if second last piece
            if index == commentLen or commentLen == 1:
                divVis("commentFooter" + divEnding, "visible")

            # censor curse words
            for key in curseWords.keys():
                commentPiece = commentPiece.replace(key, curseWords[key])

            # checks if the comment fits on the page, break out of this loop if it doesn't (this comment reply/ body gets ignored)
            height = 0
            appendDivText(commentPiece)
            mainDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "2x-container")))
            height = mainDiv.size["height"]
            if height >= 450:
                divVis("postInfo", "none")
                divVis("postInfo2", "none")
                clearCurrentDiv()
                sentenceNum = 1
                #print(commentPiece)
                appendDivText(commentPiece)
                
            time.sleep(0.5)
                        
            # take screenshot and save it
            captureHTMl(str(imageCounter))
            index += 1
            imageCounter += 1
        


def fillInCommentDetails(username, points, time):
    usernameBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usernameHere" + divEnding)))
    pointsBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pointsHere" + divEnding)))
    timeBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "timeHere" + divEnding)))

    driver.execute_script("arguments[0].innerHTML = arguments[1];", usernameBox, username)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", pointsBox, points)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", timeBox, time)


# status: hidden/visible
def divVis(divID, status):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, divID)))
    if status == "none":
        driver.execute_script("arguments[0].style.display=\'"+ status + "\'", element);
        #driver.execute_script("arguments[0].setAttribute('style','display:none;');",element)
    elif status == "visible":
        driver.execute_script("arguments[0].setAttribute('style','visibility:visible;');",element)
        #driver.execute_script("arguments[0].removeAttribute('display')", element);
    elif status == "hidden":
        driver.execute_script("arguments[0].setAttribute('style','visibility:hidden;');",element)

def writeToFile(fileName, s):
    with open(repoPath + 'Videos\\' + threadID + "\\" + commentID + "\\" + fileName + '.txt','a+') as g:
        s = re.sub(r'https?://\S+', 'https link.', s)
        s = getSpeakableString(s)
        if s == "":
            s = "blank"
        g.write(s + "\n\n\n")
    g.close()


def createDir(CommentID):
    path = repoPath + "Videos//" + threadID
    if not os.path.isdir(path):
        os.mkdir(path)

    path = path + "//" + CommentID
    if not os.path.isdir(path):
        print(CommentID)
        os.mkdir(path)


def deleteThread():
    path = "../Videos/" + threadID
    if os.path.isdir(path):
        shutil.rmtree(path)


def makeCommentsVideo():
    print("Making comments video: ", threadID)
    path = threadPath = repoPath + 'Videos\\' + threadID

    for folder in os.scandir(threadPath):
        n = 1
        firstLineBegining = 'ffmpeg -i E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\StaticTransition.mp4'
        lineEnd = ' ^ '
        filterBeginning = '-filter_complex \"[0:v][0:a]'
        mapSection = '-map [outv] -map [outa] fullComment.mp4'
        transitionPath = " -i E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\StaticTransition.mp4"
        
        firstLine = True
        #transitionPath = repoPath + "StaticTransition.mp4"
        folderDir = threadPath + "\\" + folder.name
        os.chdir(folderDir)
        fileIndex = 1
        print("Accessing:", folder.name)
        with open(folderDir + "\\pieceList.txt",'a+') as g:
            for file in os.scandir(folderDir):      
                if str(file.name).endswith('.png'):
                    #print("png: ", file.name[:-4])
                    wavName = ""
                    if os.path.isfile(str(fileIndex) + '.wav'):
                        wavName = str(fileIndex)
                    else:
                        wavName = "0" + str(fileIndex)

                    if os.path.isfile(wavName + '.wav'):
                        #print("wav:", wavName)
                        subprocess.call('ffmpeg -loop 1 -framerate 200 -i ' + str(fileIndex) + '.png -i ' + wavName + '.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out' + str(fileIndex) + '.mp4', shell=True)

                        """
                        s = "file \'out"+ str(fileIndex) +".mp4\'"
                        if firstLine:
                            firstLine = False
                            s = "file \'" + transitionPath + "\' \n" + s
                            
                        g.write(s + "\n")
                        """
                        
                        firstLineBegining = firstLineBegining + " -i out" + str(fileIndex) + ".mp4"
                        filterBeginning = filterBeginning + '[' + str(n) + ':v]['+ str(n) + ':a]'
                        n += 1
                        fileIndex += 1
                    else:
                        print("wav: N/A")
        #g.close()
                        
        filterEnd = 'concat=n='+str(n)+':v=1:a=1[outv][outa]\" ^'
        compileCode = firstLineBegining + lineEnd + filterBeginning + filterEnd + mapSection
        #print(compileCode)

        if folder.name == "Title":
            if subName == "AmITheAsshole":
                subprocess.call(compileCode, shell=True)
                os.rename("fullComment.mp4", "noMusicIntro.mp4")
                music = repoPath + "IntroMusic.mp3"
                subprocess.call('ffmpeg -i '+ music +' -i noMusicIntro.mp4 -filter_complex "[0:a]volume=0.2[a0];[1:a][a0]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[out]" -map 1:v -map "[out]" -c:v copy -shortest Intro.mp4', shell=True)
            else:
                os.rename("out1.mp4", "Intro.mp4")           
        else:
            subprocess.call(compileCode, shell=True)
        
    os.chdir(thisFilePath)
    print("Making video ended")


def combineFullComments():
    print("Combining full comments: ", threadID)
    path = threadPath = repoPath + 'Videos\\' + threadID
    os.chdir(path)
    
    n = 0
    firstLineBegining = 'ffmpeg'
    lineEnd = ' ^ '
    filterBeginning = '-filter_complex \"'
    mapSection = '-map [outv] -map [outa] VideoBody.mp4'
    transitionPath = " -i E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\StaticTransition.mp4"

    broken = False
    for folder in os.scandir(threadPath):
        if broken == True:
            break
        folderDir = threadPath + "\\" + folder.name
        if os.path.isdir(folderDir):
            for file in os.scandir(folderDir):
                if str(file.name) == "fullComment.mp4":
                    print("(Full Comment)Accessing:", folder.name)
                    firstLineBegining = firstLineBegining + " -i " + folder.name + "\\fullComment.mp4"
                    filterBeginning = filterBeginning + '[' + str(n) + ':v]['+ str(n) + ':a]'
                    n += 1

                    if n > 95:
                        broken = True
                        break
                    
    filterEnd = 'concat=n='+str(n)+':v=1:a=1[outv][outa]\" ^'
    compileCode = firstLineBegining + lineEnd + filterBeginning + filterEnd + mapSection
    print(compileCode)
    subprocess.call(compileCode, shell=True)
    #subprocess.call('ffmpeg -i eqzplik\\fullComment.mp4 -i eqzy9tl\\fullComment.mp4 -i er0g23o\\fullComment.mp4 ^ -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]\" ^-map \"[outv]\" -map \"[outa]\" CompleteVideo.mp4', shell=True)

    os.chdir(thisFilePath)


def formatTime(sec):
    if sec <= 60:
        sec = "1 minutes ago"
    elif sec < 3600:
        sec = str(math.floor(sec/60)) + " minutes ago"
    elif sec < 86400:
        sec = str(math.floor(sec/60/60)) + " hours ago"
    elif sec < 2592000:
        sec = str(math.floor(sec/60/60/24)) + " days ago"
    elif sec < 31540000:
        sec = str(math.floor(sec/60/60/24/30)) + " months ago"
    else:
        sec = "1 year ago"
    return sec


def formatPoints(points):
    if points > 999:
        remainder = points % 1000
        remainder = math.floor(remainder / 100)
        thousands = math.floor(points / 1000)

        return str(thousands) + "." + str(remainder) + "k"
    else:
        return str(points) + " points"


def getAudioFiles():
    print("Getting audio files: ", threadID)
    #time.sleep(10)
    global balabolkaFirstTimeSetup
    maxCommentVideoLength = commentVideoLength * 60
    #maxCommentVideoLength = 30
    currentThreadLength = 0
    titleAudioMade = False
    keyboard = Controller()
    threadPath = repoPath + 'Videos\\' + threadID
    # Click balabolka icon on the very left of the task bar
    mousePos((170, 1055))
    leftClick()
    
    # Open: ctrl + O
    # Split and Save: ctrl + F8

    
    for folder in os.scandir(threadPath):
        if currentThreadLength > maxCommentVideoLength and titleAudioMade == True:
            print("currentThreadLength > RequiredLength", currentThreadLength, maxCommentVideoLength)
            break
            
        folderDir = threadPath + "\\" + folder.name
        if currentThreadLength < maxCommentVideoLength or folder.name == "Title":
            if folder.name == "Title":
                titleAudioMade = True
            
            pieceCount = 0
            for file in os.scandir(folderDir):
                if str(file.name).endswith('.png'):
                    pieceCount += 1
                    
            for file in os.scandir(folderDir):   
                if str(file.name).endswith('.txt'):
                    #print("File name:", file.name)
                    txtPath = folderDir + "\\" + file.name
                    pyperclip.copy(txtPath)
                    time.sleep(0.5)
                    pressHoldRelease(('ctrl', 'o'))
                    time.sleep(0.5)
                    pressHoldRelease(('ctrl', 'v'))
                    time.sleep(0.5)
                    keyboard.press(Key.enter)
                    time.sleep(0.5)
                    pressHoldRelease(('ctrl', 'f8'))
                    pyperclip.copy(folderDir)
                    time.sleep(0.5)
                    pressHoldRelease(('ctrl', 'v'))

                    for i in range (0, 4):
                        keyboard.press(Key.tab)
                        time.sleep(0.1)
                    
                    if balabolkaFirstTimeSetup == True:
                        balabolkaFirstTimeSetup = False
                        time.sleep(0.1)
                        keyboard.press(Key.right)
                        
                    time.sleep(0.1)
                    keyboard.press(Key.tab)
                    time.sleep(0.1)
                    keyboard.press(Key.tab)
                    time.sleep(0.1)
                    keyboard.press(Key.backspace)
                    time.sleep(0.1)
                    keyboard.press(Key.tab)
                    time.sleep(0.1)
                    keyboard.press(Key.tab)
                    time.sleep(0.1)
                    keyboard.press(Key.tab)
                        
                    time.sleep(0.5)
                    keyboard.press(Key.enter)
                    time.sleep(0.5)
                    keyboard.press(Key.enter)
                    time.sleep(3 + 0.3 * pieceCount)

            for file in os.scandir(folderDir):
                if str(file.name).endswith('.wav'):
                    #print(os.getcwd())
                    f = sf.SoundFile(folderDir + "\\" + file.name)
                    seconds = len(f) / f.samplerate
                    currentThreadLength += seconds

            print("currentTotal: ", math.floor(currentThreadLength), "of", math.floor(maxCommentVideoLength))
                

    pressHoldRelease(('shift', 'ctrl', 'f4'))
    time.sleep(1)
    mousePos((170, 1055))
    leftClick()


# for pulling comments
def queueSubreddits(amount):
    global hot_python
    existingTXT = repoPath + "\\completedSubreddits.txt"
    allTXT = repoPath + "\\Subreddits.txt"
    
    i = 0
    f = open(allTXT, "r")
    #g = open(existingTXT,"r")
    existingSubs = []

    with open(existingTXT) as g:
        existingSubs = g.readlines()
    
    while i < amount:
        subID = f.readline()
        #print(subID)
        while subID in existingSubs:
            #print(subID, "exists")
            subID = f.readline()

        subID = reddit.submission(id=subID)    
        hot_python.append(subID)
        i += 1

    f.close()
    g.close()


def queueCombineFullVideo():
    threadIDs = []
    for threadID in threadIDs:
        combineFullComments(threadID)


def finishVideo():
    print("Finishing Video: ", threadID)
    path = repoPath + 'Videos\\' + threadID
    music = repoPath + "SelectedSoundtrack.mp3"
    intro = path + "\\Title\\Intro.mp4"
    endTro = repoPath + "Outtro.mp4"
    os.chdir(path)
    # add music
    #print('ffmpeg -i '+ music +' -i VideoBody.mp4 -filter_complex "[0:a]volume=0.2[a0];[1:a][a0]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[out]" -map 1:v -map "[out]" -c:v copy -shortest BodyWithMusic.mp4')
    subprocess.call('ffmpeg -i '+ music +' -i VideoBody.mp4 -filter_complex "[0:a]volume=0.2[a0];[1:a][a0]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[out]" -map 1:v -map "[out]" -c:v copy -shortest BodyWithMusic.mp4', shell=True)
    
    # combine with endtro and intro
    #print('ffmpeg -i ' + intro + ' -i BodyWithMusic.mp4 -i ' + endTro + ' ^ -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]\" ^-map \"[outv]\" -map \"[outa]\" CompleteVideo.mp4')
    subprocess.call('ffmpeg -i ' + intro + ' -i BodyWithMusic.mp4 -i ' + endTro + ' ^ -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]\" ^-map \"[outv]\" -map \"[outa]\" CompleteVideo.mp4', shell=True)


def markAsCompleted():
    global startTime
    subredditsTxt = repoPath + "\\completedSubreddits.txt"
    with open(subredditsTxt,'a+') as g:
        g.write(str(threadID) + "\n Duration: " + str(math.floor((time.time() - startTime) / 60)) + " minutes \n\n")
        startTime = time.time()
    g.close()


def commentVisiblitySetting(visSetting):
    if visSetting == "firstComment":
        divVis("threadLineAlign", "visible")
        divVis("threadLineAlignR", "none")
        divVis("upDownButtons", "hidden")
        divVis("otherInfo", "none")
        
    elif visSetting == "secondComment":
        divVis("commentWhole", "none")
        divVis("threadLineAlign", "none")
        divVis("threadLineAlignR", "visible")
        divVis("upDownButtons", "none")
        divVis("upDownButtonsR", "hidden")
        divVis("otherInfoR", "none")
        divVis("commentFooter", "none")

"""
- Iterates over post -> comments in post -> replies to comments -> comment broken up into section
"""    
# runs at the start
def main():
    global sentenceNum
    global divEnding
    global driver
    global threadID
    global commentID
    global commentVideoLength
    startDriver()

    # minutes
    commentVideoLength = 10
    queueSubreddits(5)
    getComments()
       
    # Iterates over every post
    for key in commentDict.keys():
        threadID = str(key)
        commentIndex = 0

        questionHTMLName = "Question"
        if subName == "AmItheAsshole":
            questionHTMLName = questionHTMLName + "AITA"
            
        driver.get("http://localhost//"+localServerFolder+"//" + questionHTMLName + ".html")
        getThreadOpeningVideo()

        # Iterates over every comment in that post
        for comment in commentDict[key]:
            driver.get("http://localhost//"+localServerFolder+"//Comments.html")
            print("\n\n\nMaking Comment Folders: ", threadID)
            #comment = reddit.comment(id="eiu28ff")

            commentID = str(comment)
            # image counter is used for saving as a screenshot
            imageCounter = 1
            # commentIndex is used for saving a .txt file for the comment number
            commentIndex += 1
            # divEnding is used for when editing the html for a comment
            divEnding = ""
            
            # Hide the footer and clear the text
            divVis("commentFooter", "none")
            divVis("commentFooterR", "none")
            divVis("mainDivR", "none")
            clearDiv()
            
            # Gets the amount of replies
            repliesAmount = 0
            if commentID in commentReplies.keys():
                repliesAmount = len(commentReplies[commentID])

            # Iterate over the main comment and the amount of replies
            for i in range(0, repliesAmount + 1):
                # if it is a reply rather than the main comment
                if i != 0:
                    comment = commentReplies[commentID][0]
                    divEnding = "R"
                    divVis("mainDivR", "visible")

                # sentenceNum is used for the paragraph index when writing to the HTML file
                sentenceNum = 1
                
                authorName = "deleted"
                if hasattr(comment.author, 'name'):
                    authorName = comment.author.name
                
                fillInCommentDetails(authorName, formatPoints(comment.score), formatTime(time.time() - comment.created_utc))
                createDir(commentID)
                commentBody = comment.body
                #commentBody = "It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. \n\nIt was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. \n\n Lorem Ipsum is simply dummy text of the printing and typesetting industry. \n\nLorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. \n\nIt was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.Lorem Ipsum is simply dummy text of the printing and typesetting industry. \n\nLorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. \n\nIt has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially"
                comment = splitComment(commentBody)
                commentLen = len(comment)
                
                # checks if the comment fits on the page, break out of this loop if it doesn't (this comment reply/ body gets ignored)
                height = 0

                # index is used for displaying the footer when the comment is coming to an end
                index = 1
                # sentenceNum is used for the paragraph index when writing to the HTML file
                sentenceNum = 1
                # Iterate over every comment piece
                for commentPiece in comment:
                    mainDiv = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "2x-container")))
                    height = mainDiv.size["height"]
                    #print("height:", height)
                    if height >= 480:
                        #print("Comment has reached the screen limit")
                        commentVisiblitySetting("firstComment")
                        clearSpecifiedDiv("")

                        if divEnding == "R":
                            #print("Comment type: Reply")
                            commentVisiblitySetting("secondComment")
                            clearSpecifiedDiv("R")
                            
                        else:
                            pass
                            #print("Comment type: First/Main")

                        sentenceNum = 1
                         
                    # write to file
                    writeToFile(str(commentIndex), commentPiece)
                        
                    # if second last piece
                    if index == commentLen or commentLen == 1:
                        divVis("commentFooter" + divEnding, "visible")

                    # censor curse words
                    for key in curseWords.keys():
                        commentPiece = commentPiece.replace(key, curseWords[key])
                        
                    appendDivText(commentPiece)
                    time.sleep(0.5)
                        
                    # take screenshot and save it
                    captureHTMl(str(imageCounter))
                    index += 1
                    imageCounter += 1

            #break

        getAudioFiles()
        makeCommentsVideo()
        combineFullComments()
        finishVideo()
        markAsCompleted()
        
    driver.quit()


def queueQuestionsIntoFile():
    global hot_python
    existingTXT = repoPath + "\\SubReddits.txt"
    allTXT = repoPath + "\\SubredditsFull.txt"
    
    i = 0
    f = open(allTXT, "r")
    g = open(existingTXT,"a+")
    existingSubs = []
    
    while i < 1100:
        subID = f.readline()
        subID.replace("\n", "")
        if subID != "\n" and subID != "":
            subID = subID[0:7]
            g.write(subID + "\n")

        i += 1

    f.close()
    g.close()


def makeThumbnail(index):
    text = "#"+index
    x = 930
    y = 25
    fillcolor = "#EAD223"
    shadowcolor = "black"
    borderThickness = 7
    imgPath = "E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\Images\\ThumbailTemplate2.png"
    font = ImageFont.truetype("E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\Bubblegum.ttf", 180)
    im = Image.open(imgPath)
    draw = ImageDraw.Draw(im)
    
    # thicker border
    draw.text((x-borderThickness, y-borderThickness), text, font=font, fill=shadowcolor)
    draw.text((x+borderThickness, y-borderThickness), text, font=font, fill=shadowcolor)
    draw.text((x-borderThickness, y+borderThickness), text, font=font, fill=shadowcolor)
    draw.text((x+borderThickness, y+borderThickness), text, font=font, fill=shadowcolor)
    draw.text((x, y), text, font=font, fill=fillcolor)
    
    fname2 = "E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\Images\\Thumbnails\\" + index + ".jpg"
    im.save(fname2)
    #os.startfile(fname2)

#for i in range(1, 100):
#    makeThumbnail(str(i))

#getTopSubredditPosts()
main()
#threadID = "cf1lbg"
#queueQuestionsIntoFile()
#testReplacement()
#getAudioFiles()
#makeCommentsVideo()
#combineFullComments()
#finishVideo()
#getTopSubredditPosts()

"""
    Notes on global variables:
    1. declare global if global variable is going to be changed
    2. does not have to be declared global if it is only to be used and not changed
    3. if declared local it can be changed but only locally and the global cannot be used
    4. can be passed as a parameter as long as it is not declared global 
"""
