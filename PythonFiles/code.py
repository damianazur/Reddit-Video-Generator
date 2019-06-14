import os, sys, time
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

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import shutil

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
hot_python= subreddit.hot(limit = 1)

commentDict = {}

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

def captureHTMl(srcNum):
    driver.get("http://localhost//TalkReddit//Comments.html")
    driver.execute_script("document.body.style.zoom='250%'")
    driver.save_screenshot("attempt"+ srcNum +".png")
    driver.quit()

def copyFile():
    shutil.copy2('C://xampp//htdocs//TalkReddit//Comments_Base.html', 'C://xampp//htdocs//TalkReddit//Comments.html')
 

# runs at the start
def main():
    getComments(1)
    printComments()
    startDriver()
    copyFile()
    captureHTMl()
 
if __name__ == '__main__':
    main()

