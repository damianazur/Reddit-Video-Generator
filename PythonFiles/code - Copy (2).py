import os, sys, time
import subprocess
import time, random
from random import randrange
from numpy import *
import re

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import shutil

thisFilePath = os.getcwd()
os.chdir('..')
repoPath = os.getcwd() + "\\" 
os.chdir(thisFilePath)
print(repoPath)
print(os.getcwd())

chromePath = repoPath + "chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless')
chromeOptions.add_argument(f'window-size={1920}x{1080}')
driver = 0

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

subreddit = reddit.subreddit('askreddit')
submission2 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c01upz/you_can_fill_a_pool_with_anything_you_want_money/')
submission1 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c193hp/whats_the_most_disturbing_secret_youve_been_told/')
#hot_python = subreddit.hot(limit = 1)
hot_python = [submission1]

commentDict = {}
endCharacters = ['.', ',', '?', '!']
otherCharacters = ["“", "\""]

def getComments(amount):
    for submission in hot_python:
        if not submission.stickied:
            print(submission.title, "\n")

            # comments in thread
            submission.comments.replace_more(limit = 0)
            commentCount = 0
            for comment in submission.comments.list():
                # comment is the first comment
                if comment.parent() == submission:
                    #if commentCount == 0:
                        #print(dir(comment))
                    
                    # key exists
                    if comment.parent() in commentDict:
                        commentDict[comment.parent()].append(comment)
                    # key does not exist
                    else:
                        commentDict[comment.parent()] = [comment]

                    commentCount += 1
                    if commentCount >= amount:
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
    driver.get("http://localhost//TalkReddit//Comments.html")

def captureHTMl(srcNum, threadID, commentID):
    #driver.get("http://localhost//TalkReddit//Comments.html")
    driver.execute_script("document.body.style.zoom='200%'")
    driver.save_screenshot(repoPath + 'Videos\\' + threadID + "\\" + commentID + "\\" + srcNum + ".png")
    #driver.quit()

def copyFile():
    shutil.copy2('C://xampp//htdocs//TalkReddit//Comments_Base.html', 'C://xampp//htdocs//TalkReddit//Comments.html')

def cleanString(s):
    pass

def splitComments():
    comments = []
    
    for commentArray in commentDict.values():
        for comment in commentArray:
            print(20*'-')
            sentences = []
            sIndex = 0
            endIndex = 0
            commentBody = comment.body
            print(commentBody)
            commBodyLen = len(commentBody)
            for char in commentBody:
                endIndex += 1
                if ( endIndex == commBodyLen or char == '.' and commentBody[endIndex] != '.' or char == ',' and not commentBody[endIndex - 2].isdigit() or char == '?'):
                    sentence = commentBody[sIndex:endIndex]
                    sentence = cleanString(sentence)
                    sIndex = endIndex
                    sentences.append(sentence)
                    #print(sentence)

            comments.append(sentences)
            #break
            
    return comments

def splitComment(commentBody):
    global endCharacters
    global otherCharacters
    sentences = []
    sIndex = 0
    endIndex = 0
    #print(commentBody)
    commentBody = commentBody.replace('\n', '<br>')
    commBodyLen = len(commentBody)

    while endIndex < commBodyLen:
        #print(commentBody[endIndex])
        if commentBody[endIndex] in endCharacters:
            endIndex += 1
            #print(commBodyLen, endIndex)
            #if endIndex < commBodyLen:
            while endIndex < commBodyLen and (commentBody[endIndex] in endCharacters or commentBody[endIndex] in otherCharacters or commentBody[endIndex].isdigit()):
                print("Going through")
                endIndex += 1

            sentence = commentBody[sIndex:endIndex]
            sIndex = endIndex
            sentences.append(sentence)

        endIndex += 1

    sentence = commentBody[sIndex:endIndex]
    sentences.append(sentence)
            
    """
    for char in commentBody:
        endIndex += 1
        if ( endIndex == commBodyLen or char == '.' and
             commentBody[endIndex] != '.' or char == ',' and
             not commentBody[endIndex - 2].isdigit() or char == '?'):
            
            sentence = commentBody[sIndex:endIndex]
            sIndex = endIndex
            sentences.append(sentence)
    """

    return sentences

def replaceText(newText):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    textDivElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    #print("InnerHTML: " + textDivElement.get_attribute('innerHTML'))
    #newText = element.text + newText
    #print(newText)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)

def appendDivText(newText):
    brEndFound = False
    brStartFound = False
    if newText[-8:] == "<br><br>":
        brEndFound = True
    
    textDivElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    oldText = textDivElement.get_attribute('innerHTML')

    if "<br><br>" in newText[:11]:
        brStartFound = True
        oldText = oldText + '<p class=' + '"rz6fp9-10 himKiy"' + 'id=\"commentBodyText">'
    
    newText = newText.replace("<br><br>", "")

    if oldText[-4:] == "</p>":
        oldText = oldText[:-4]
    newText = oldText + newText + "</p>"

    if brEndFound == True:
        newText = newText + '<p class=' + '"rz6fp9-10 himKiy"' + 'id=\"commentBodyText">'
    
    driver.execute_script("arguments[0].innerHTML = arguments[1];", textDivElement, newText)
    #print("---------------------------\n", textDivElement.get_attribute('innerHTML'))

def clearText():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    newText = ""
    driver.execute_script("arguments[0].textContent = arguments[1];", element, newText)

def clearDiv():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    newText = ""
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)

def fillInCommentDetails(username, points, time):
    usernameBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usernameHere")))
    pointsBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pointsHere")))
    timeBox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "timeHere")))

    driver.execute_script("arguments[0].innerHTML = arguments[1];", usernameBox, username)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", pointsBox, points)
    driver.execute_script("arguments[0].innerHTML = arguments[1];", timeBox, time)

# status: hidden/visible
def divVis(divID, status):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, divID)))
    driver.execute_script("arguments[0].style.visibility=\'"+ status + "\'", element);

def writeToFile(fileName, s, threadID, commentID):
    with open(repoPath + 'Videos\\' + threadID + "\\" + commentID + "\\" + fileName + '.txt','a+') as g:
        s = s.replace("<br>", "")
        s = re.sub(r'[^\x00-\x7F]+',' ', s)
        g.write(s + "\n\n\n")
    g.close()

def createDir(threadID, CommentID):
    path = "../Videos/" + threadID
    if not os.path.isdir(path):
        os.mkdir(path)

    path = path + "/" + CommentID
    if not os.path.isdir(path):
        print("comment path doesn't exist")
        os.mkdir(path)
    # if a folder for a comment already exists then remove the comment folder and create a new one under the same comment ID
    #else:
        #print("comment path already")
        #shutil.rmtree(path)
        #os.mkdir(path)

def deleteThread(threadID):
    path = "../Videos/" + threadID
    if os.path.isdir(path):
        shutil.rmtree(path)

def makeVideo(threadID, commentID):
    videoArray = []
    print("Making video")
    path = repoPath + 'Videos\\' + threadID + "\\" + commentID
    os.chdir(path)
    print(os.getcwd())
    #subprocess.call('ffmpeg -loop 1 -framerate 30 -i 1.png -i 01.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest outt1.mp4', shell=True)
    #subprocess.call('ffmpeg -loop 1 -framerate 30 -i ' + str(i) + '.png -i ' + wavName + '.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest outt' + str(i) + '.mp4', shell=True)
    #                 ffmpeg -r 1 -loop 1 -i 1.png -i 01.wav -c:v libx264 -acodec copy -r 1 -shortest ep1.flv
    
    for i in range (1, 8):
        wavName = str(i)
        if i < 10:
            wavName = "0" + str(i)
            
        subprocess.call('ffmpeg -loop 1 -framerate 200 -i ' + str(i) + '.png -i ' + wavName + '.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out' + str(i) + '.mp4', shell=True)
        #videoArray.append("out" + str(i))
    #subprocess.call('ffmpeg -f concat -i soundOrder.txt -c copy outputX.wav', shell=True)
    os.chdir(thisFilePath)
    print("Making video ended")
    #concatVideos(videoArray)
    
def concatVideos(videoArray, cwd):
    path = repoPath + 'Videos\\c193hp\\erc08i0'
    os.chdir(path)
    subprocess.call('ffmpeg -safe 0 -f concat -i list2.txt -c copy output.mp4', shell=True)

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
        
    
# runs at the start
def main():
    getComments(10)
    startDriver()
    copyFile()
    commentIndex = 0

    global submission1
    threadID = str(submission1)
    deleteThread(threadID)
    for key in commentDict.keys():
        for comment in commentDict[key]:
            fillInCommentDetails(comment.author.name, formatPoints(comment.score), formatTime(time.time() - comment.created_utc))
            start = True
            htmlText = '<p class=' + '"rz6fp9-10 himKiy"' + 'id=\"commentBodyText">'
            imageCounter = 1
            commentID = str(comment)
            createDir(threadID, commentID)
            commentBody = comment.body
            comment = splitComment(commentBody)
            
            commentLen = len(comment)
            index = 1
            commentIndex += 1
            divVis("commentFooter", "hidden")
            clearDiv()
            for commentPiece in comment:
                # write to file
                writeToFile(str(commentIndex), commentPiece, threadID, commentID)
                
                # if second last piece 
                if index == commentLen or commentLen == 1:
                    divVis("commentFooter", "visible")
                    
                # add text
                if start == True :
                    commentPiece = htmlText + commentPiece
                    start = False
                appendDivText(commentPiece)
                time.sleep(0.5)
                
                # take screenshot and save it
                captureHTMl(str(imageCounter), threadID, commentID)
                index += 1
                imageCounter += 1

            #makeVideo(threadID, commentID)

    """
    comments = splitComments()
    for comment in comments:
        commentLen = len(comment)
        index = 1
        commentIndex += 1
        divVis("commentFooter", "hidden")
        clearText()
        for commentPiece in comment:
            # write to file
            writeToFile(str(commentIndex), commentPiece)
            
            # if second last piece 
            if index == commentLen or commentLen == 1:
                divVis("commentFooter", "visible")
                
            # add text
            replaceText(commentPiece)
            time.sleep(0.5)
            # take screenshot and save it
            captureHTMl(str(imageCounter))
            index += 1
            imageCounter += 1
    """
    
    driver.quit()

def testVoices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice)
    
        #if voice.languages[0] == u'en_US':
        #    engine.setProperty('voice', voice.id)
        #    break

    #engine.say('Hello World')
    #engine.runAndWait()

def testText():
    getComments(50)
    printComments()

     
#writeToFile("1", "String")
makeVideo("c193hp", "erc08i0")
#concatVideos(1, 2)
#main()
#testText()
#deleteThread("c01upz")
#testVoices()


