import os, sys, time
import subprocess
import time, random
from random import randrange
from numpy import *
import win32api, win32con
from win32con import *
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

import soundfile as sf

thisFilePath = os.getcwd()
os.chdir('..')
repoPath = os.getcwd() + "\\" 
os.chdir(thisFilePath)

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

submission3 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c01upz/you_can_fill_a_pool_with_anything_you_want_money/')
submission2 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c193hp/whats_the_most_disturbing_secret_youve_been_told/')
submission1 = reddit.submission(url='https://www.reddit.com/r/AskReddit/comments/c4p6l1/what_happened_at_your_work_which_caused_multiple/')
#hot_python = subreddit.hot(limit = 1)
hot_python = []

commentDict = {}
questionDict = {}
urlEndings = [".com", ".html", ".uk", ".php", ".html", ".org", ".net", ".eu"]
endCharacters = ['.', ',', '?', '!']
otherCharacters = ["“", "\""]
balabolkaFirstTimeSetup = False

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

def getTopSubredditPosts():
    top_askreddits = subreddit.top(limit = 10000)
    subredditsTxt = repoPath + "\\Subreddits.txt"
    with open(subredditsTxt,'a+') as g:
        for sub in top_askreddits:
            title = re.sub(r'[^\x00-\x7F]+','\'', sub.title)
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

def getComments(amount):
    global questionDict
    for submission in hot_python:
        if not submission.stickied:
            print(submission.title, "\n")

            authorName = "deleted"
            if hasattr(submission.author, 'name'):
                authorName = submission.author.name
                
            numComments = formatPoints(submission.num_comments)
            createdTime = formatTime(time.time() - submission.created_utc)
            score = formatPoints(submission.score)
            
            questionDict[str(submission)] = {"title" : submission.title, "author" : authorName, "numComments" : numComments, "createdTime" : createdTime, "score" : score}
            
            #print("submission title: ", questionDict[str(submission)]["title"])
            
            # comments in thread
            submission.comments.replace_more(limit = 0)
            commentCount = 0
            for comment in submission.comments.list():
                # comment is the first comment
                if comment.parent() == submission:
                    #if commentCount == 0:
                        #print(dir(comment))

                    if len(comment.body) < 1500:
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
    driver.execute_script("document.body.style.zoom='150%'")
    driver.save_screenshot(repoPath + 'Videos\\' + threadID + "\\" + commentID + "\\" + srcNum + ".png")

def copyFile():
    shutil.copy2('C://xampp//htdocs//TalkReddit//Comments_Base.html', 'C://xampp//htdocs//TalkReddit//Comments.html')

def splitComment(commentBody):
    global endCharacters
    global otherCharacters
    global urlEndings
    sentences = []
    sIndex = 0
    endIndex = 0
    commentBody = commentBody.replace('\n', '<br>')
    commentBody = commentBody.strip() 
    commBodyLen = len(commentBody)

    while endIndex < commBodyLen:
        if commentBody[endIndex:endIndex + 6] == "https:":
            while endIndex < commBodyLen - 1 and commentBody[endIndex] != " ":
                endIndex += 1
        
        if commentBody[endIndex] in endCharacters:
            endIndex += 1
            while endIndex < commBodyLen and (commentBody[endIndex] in endCharacters or commentBody[endIndex] in otherCharacters or commentBody[endIndex].isdigit()):
                #print("Going through")
                endIndex += 1

            if not commentBody[endIndex - 1].isdigit():
                sentence = commentBody[sIndex:endIndex]
                sIndex = endIndex
                sentences.append(sentence)

        endIndex += 1

    if sIndex != endIndex and commentBody[sIndex:endIndex] != "":
        sentence = commentBody[sIndex:endIndex]
        #print("-#-", sentence)
        sentences.append(sentence)

    return sentences

def replaceText(newText):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    textDivElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
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

def clearText():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyText")))
    newText = ""
    driver.execute_script("arguments[0].textContent = arguments[1];", element, newText)

def clearDiv():
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commentBodyDiv")))
    newText = ""
    driver.execute_script("arguments[0].innerHTML = arguments[1];", element, newText)

def getThreadOpeningVideo(threadID):
    global questionDict
    createDir(threadID, "Title")
    
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
    time.sleep(0.5)
    driver.save_screenshot(repoPath + 'Videos\\' + threadID + "\\Title\\1.png")
    writeToFile("title", questionDict[threadID]["title"], threadID, "Title")


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
        s = re.sub(r'[^\x00-\x7F]+','\'', s)
        s = re.sub(r'https?://\S+', '', s)
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

def makeCommentsVideo(threadID):
    print("Making video")
    path = threadPath = repoPath + 'Videos\\' + threadID

    for folder in os.scandir(threadPath):
        folderDir = threadPath + "\\" + folder.name
        os.chdir(folderDir)
        fileIndex = 1
        print("Accessing:", folder.name)
        with open(folderDir + "\\pieceList.txt",'a+') as g:
            for file in os.scandir(folderDir):      
                if str(file.name).endswith('.png'):
                    print("png: ", file.name[:-4])
                    wavName = ""
                    if os.path.isfile(str(fileIndex) + '.wav'):
                        wavName = str(fileIndex)
                    else:
                        wavName = "0" + str(fileIndex)

                    if os.path.isfile(wavName + '.wav'):
                        print("wav:", wavName)
                        subprocess.call('ffmpeg -loop 1 -framerate 200 -i ' + str(fileIndex) + '.png -i ' + wavName + '.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out' + str(fileIndex) + '.mp4', shell=True)
                        s = "file \'out"+ str(fileIndex) +".mp4\'"
                        g.write(s + "\n")
                    
                        fileIndex += 1
                    else:
                        print("wav: N/A")
        g.close()

        #print(fileIndex)
        if fileIndex == 2:
            #print("renaming")
            os.rename('out1.mp4', 'fullComment.mp4')
        else:
            subprocess.call('ffmpeg -safe 0 -f concat -i pieceList.txt -c copy fullComment.mp4', shell=True)

        fullCommentCompiled = False
        for file in os.scandir(folderDir):
            if file.name == "fullComment.mp4":
                fullCommentCompiled = True
        
        if fullCommentCompiled:
            subprocess.call('ffmpeg -i fullComment.mp4 -r 30 -y fullComment2.mp4', shell=True)
            os.remove("fullComment.mp4")
            if folder.name == "Title":
                os.rename("fullComment2.mp4", "Intro.mp4")
            else:
                os.rename("fullComment2.mp4", "fullComment.mp4")

    os.chdir(thisFilePath)
    print("Making video ended")

def combineFullComments(threadID):
    path = threadPath = repoPath + 'Videos\\' + threadID
    os.chdir(path)
    
    n = 0
    firstLineBegining = 'ffmpeg'
    lineEnd = ' ^ '
    filterBeginning = '-filter_complex \"'
    mapSection = '-map [outv] -map [outa] VideoBody.mp4'
    transitionPath = " -i E:\\Users\\User1\\Documents\\Git\\VideoMakerRepo\\StaticTransition.mp4"

    for folder in os.scandir(threadPath):
        folderDir = threadPath + "\\" + folder.name
        if os.path.isdir(folderDir):
            for file in os.scandir(folderDir):
                if str(file.name) == "fullComment.mp4":
                    print("(Full Comment)Accessing:", folder.name)
                    firstLineBegining = firstLineBegining + transitionPath + " -i " + folder.name + "\\fullComment.mp4"
                    filterBeginning = filterBeginning + '[' + str(n) + ':v]['+ str(n) + ':a]' + '[' + str(n+1) + ':v]['+ str(n+1) + ':a]'
                    n += 2
                    
    filterEnd = 'concat=n='+str(n)+':v=1:a=1[outv][outa]\" ^'
    compileCode = firstLineBegining + lineEnd + filterBeginning + filterEnd + mapSection
    #print(compileCode)
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

def getAudioFiles(threadID, maxCommentVideoLength):
    #time.sleep(10)
    global balabolkaFirstTimeSetup
    maxCommentVideoLength = maxCommentVideoLength * 60
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
                    print(os.getcwd())
                    f = sf.SoundFile(folderDir + "\\" + file.name)
                    seconds = len(f) / f.samplerate
                    currentThreadLength += seconds
            print("currentTotal: ", currentThreadLength)
                

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
    g = open(existingTXT,"r")
    
    while i < amount:
        subID = f.readline()
        print(subID)
        while subID in open(existingTXT).read():
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

def finishVideo(threadID):
    path = repoPath + 'Videos\\' + threadID
    music = repoPath + "SelectedSoundTrack.mp3"
    intro = path + "\\Title\\Intro.mp4"
    endTro = repoPath + "Outtro.mp4"
    os.chdir(path)
    # add music
    subprocess.call('ffmpeg -i '+ music +' -i VideoBody.mp4 -filter_complex "[0:a]volume=0.2[a0];[a0][1:a]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[out]" -map 1:v -map "[out]" -c:v copy -shortest BodyWithMusic.mp4', shell=True)
    
    # combine with endtro and intro
    subprocess.call('ffmpeg -i ' + intro + ' -i BodyWithMusic.mp4 -i ' + endTro + ' ^ -filter_complex \"[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]\" ^-map \"[outv]\" -map \"[outa]\" CompleteVideo.mp4', shell=True)
    
# runs at the start
def main():
    startDriver()
    global driver
    #copyFile()
    queueSubreddits(1)
    getComments(15)
    
    #global submission1
    #threadID = str(submission1)
    threadID = 0
    #deleteThread(threadID)

    driver.get("http://localhost//TalkReddit//Question.html")
    for key in commentDict.keys():
        threadID = str(key)
        getThreadOpeningVideo(threadID)
        commentIndex = 0
        driver.get("http://localhost//TalkReddit//Comments.html")
        for comment in commentDict[key]:
            authorName = "deleted"
            if hasattr(comment.author, 'name'):
                authorName = comment.author.name
                
            fillInCommentDetails(authorName, formatPoints(comment.score), formatTime(time.time() - comment.created_utc))
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
                #print("-", commentPiece)
                # write to file
                writeToFile(str(commentIndex), commentPiece, threadID, commentID)
                
                # if second last piece 
                if index == commentLen or commentLen == 1:
                    divVis("commentFooter", "visible")
                    
                # add text
                if start == True:
                    commentPiece = htmlText + commentPiece
                    start = False
                appendDivText(commentPiece)
                time.sleep(0.5)
                
                # take screenshot and save it
                captureHTMl(str(imageCounter), threadID, commentID)
                index += 1
                imageCounter += 1

        subredditsTxt = repoPath + "\\completedSubreddits.txt"
        with open(subredditsTxt,'a+') as g:
            g.write(str(threadID) + "\n")           
        g.close()

        # minutes
        commentVideoLength = 1
        getAudioFiles(threadID, commentVideoLength)
        makeCommentsVideo(threadID)
        combineFullComments(threadID)
        
    driver.quit()
    #getAudioFiles(threadID)
    #makeCommentsVideo(threadID)
    #combineFullComments(threadID)

     
#writeToFile("1", "String")
#concatVideos(1, 2)
#main()
#getAudioFiles("80phz7", 15)
#makeCommentsVideo("80phz7")
#combineFullComments("80phz7")
#getTopSubredditPosts()
finishVideo("80phz7")
