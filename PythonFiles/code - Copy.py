import os, sys, time
import subprocess
#import PIL
#from PIL import Image, ImageGrab, ImageOps
import time, random
from random import randrange
#import win32api, win32con
#from win32con import *
from numpy import *
#import pyperclip
#import imgkit
#import pdfkit
#import wkhtmltopdf
#from wkhtmltopdf import WKhtmlToPdf
#import ffmpeg

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import shutil
#import pyttsx3



chromePath = "C:\\Users\\User1\\Downloads\\OCALL\\chromedriver.exe"
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
submission1 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c01upz/you_can_fill_a_pool_with_anything_you_want_money/')
#hot_python = subreddit.hot(limit = 1)
hot_python = [submission1]

commentDict = {}

repoPath = 'C:\\Users\\User1\\Desktop\\Talk Reddit\\VideoMakerRepo\\'
imagePath = repoPath + 'Image Files\\'
soundPath = repoPath + 'Sound Files\\'
videosPath = repoPath + 'Videos\\'

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
            print(comment.body)

def startDriver():
    global driver
    driver = webdriver.Chrome(executable_path = chromePath, options = chromeOptions)
    driver.get("http://localhost//TalkReddit//Comments.html")

def captureHTMl(srcNum):
    #driver.get("http://localhost//TalkReddit//Comments.html")
    driver.execute_script("document.body.style.zoom='200%'")
    driver.save_screenshot('C:\\Users\\User1\\Desktop\\Talk Reddit\\VideoMakerRepo\\Image Files\\' + "attempt" + srcNum + ".png")
    #driver.quit()

def copyFile():
    shutil.copy2('C://xampp//htdocs//TalkReddit//Comments_Base.html', 'C://xampp//htdocs//TalkReddit//Comments.html')

def splitComment():
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
                    sIndex = endIndex
                    sentences.append(sentence)
                    #print(sentence)

            comments.append(sentences)
            #break

    return comments

def replaceText(newText):
    #driver.execute_script("""document.querySelector("username_here");""")
    #inputElement = driver.find_element_by_id('commentBodyText')
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    newText = element.text + newText
    #print("newText:", newText)
    #driver.execute_script("arguments[0].innerText = \'" +"\\"+ str(newText)+"\\"+ "\'", element)
    driver.execute_script("arguments[0].textContent = arguments[1];", element, newText)

def clearText():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    newText = ""
    driver.execute_script("arguments[0].textContent = arguments[1];", element, newText)

# status: hidden/visible
def divVis(divID, status):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, divID)))
    driver.execute_script("arguments[0].style.visibility=\'"+ status + "\'", element);

def writeToFile(fileName, s):
    with open('C:\\Users\\User1\\Desktop\\Talk Reddit\\VideoMakerRepo\\TXT Files\\' + fileName + '.txt','a+') as g:
        g.write(s + "\n\n")
    g.close()

def createDir(threadID, CommentID):
    path = "../Videos/" + threadID
    if os.path.isdir(path):
        print("path exists")
        #shutil.rmtree()
    else:
        os.mkdir(path)
        path = path + "/" + CommentID
        os.mkdir(path + "/Audio")
        os.mkdir(path + "/Image")
        os.mkdir(path + "/Vide")

def makeVideo():
    index = 4
    #print( os.getcwd() )
    #os.chdir('C://Users/User1/Desktop/Talk Reddit/VideoMakerRepo/PythonFiles/')
    subprocess.call('ffmpeg -loop 1 -i imageFile.png -i audioFile.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out6.mp4', shell=True)
    
# runs at the start
def main():
    getComments(1)
    #printComments()
    startDriver()
    copyFile()
    comments = splitComment()
    #print(comments[0])
    imageCounter = 1
    commentIndex = 0
    
    for comment in comments:
        break
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
     
if __name__ == '__main__':
    #writeToFile("1", "String")
    #makeVideo()
    main()
    #createDir("Title")
    #testVoices()

