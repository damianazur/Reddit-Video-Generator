# Reddit Video Maker

A program coded in Python that automatically creates a narrated video of a Reddit topic/question, the question and replies to it are read out.<br>
It is like browsing Reddit but made into a video that can then be automatically uploaded to youtube.<br>
Product of the program: https://youtu.be/SE9KLY-UQck <br>
Youtube channel: https://www.youtube.com/channel/UCr2PCTA71fdEs1HHD6eLcJQ <br>
Videos in a very similar format can get as much a coupe million views on youtube: https://youtu.be/GdFvd7KDNmQ

## How it works

**Video Creation:** <br><br>
<img src="https://i.imgur.com/sK7YuHS.png" width="90%" height="90%">
<img src="https://i.imgur.com/HdBeWzD.png" width="90%" height="90%">
- The python file is opened in IDLE (64-bit) and run by pressing F5
- Program asks for you to enter arguments such as the length of the video, how many video's to create and what kind of video's to create.
- Program will obtain the topic's question and comments using a Reddit API (PRAW) and store it in a dictionary.
- The questiona and comment text is split into sections (these will appear on screen as soon as they are read out)
- On a local webserver each text section will be added in and a screenshot will be taken (screenshot taken in the background). These images will be the frames for the video.
- The text sections will also be saved to a text file which will then be using to obtain the audio files for the video using a 3rd party software Balabolka. 
- The images and audio are combined to make a video using FFMPEG
- Video sections are combined, then music, intro and outtro are added

<br>**Video Uploading:**
- Uploads using the Google Youtube API
- User is given a link and a prompt, following the link they will have to login to their youtube account and a code will be given to them. The program will be able to upload videos after the code is entered. <br><br> <img src="https://imgur.com/f3yDxTu.png" width="90%" height="90%">
- Video's are scheduled to be uploaded every 6 hours

<br>**Other Features:**
- The program automatically creates thumbanils for the youtube videos <img src="https://i.imgur.com/VncQA5Z.png" width="90%" height="90%">
- Because of headless chrome images/screenshots for the video are the same on any computer regardless of the screen size and are obtained in the background.
- The program automatically queues video's for uploading, keeps tracks of which videos have been created, uploaded, when the next video should be uploaded and what the next thumbnail for the video is.

## Prerequisites
These are the things needed to get the program fully working

**1. Python Libraries** <br>
- pillow: For automatically making thumbnails (editing images)
- selenium: For opening a HTML file in the background, changing information in the local web page and taking screenshots
- soundfile: For making sure the video/audio is of a certain length
- praw: Reddit API for scaping/obtaining data from a subreddit/thread
- shutil: For moving/copying files
- pyperclip: Copying text to clipboard
 -win32con, win32api: Clicking on the screen
- pynput: For using a virtual keyboard for automation<br>
- Install with PIP:<br>
pip install pillow, selenium, soundfile, praw, pytest-shutil, pyperclippypiwin32, pynput

**2. Reddit API application setup (Scrapes data from reddit)**<br>
- Sentdex has a great video on how to set it up:<br>
[How to set up Reddit API Video](https://www.youtube.com/watch?v=NRgfgtzIhBQ/)

**3. XAMPP Local Website Hosting - Apache (The local HTML file can be hosted using XAMPP so Headless Chrome can use it)**<br>
- [XAMPP Download](https://www.apachefriends.org/index.html) 
- XAMPP Apache up and running: <img src="https://i.imgur.com/bztG0e7.png">
- If it fails to run make sure to allow the program through windows firewall:<br>
[How to allow an app through windows firewall](https://pureinfotech.com/allow-apps-firewall-windows-10/)

**4. FFMPEG Static Version (Combines image and audio files to make a video)**<br>
- To make sure it is working type in "ffmpeg" into command prompt. If there is an error an environmental variable has to be set up
- [FFMPEG Download](https://ffmpeg.zeranoe.com/builds/)
- [Setting up environmental variable for FFMPEG](https://video.stackexchange.com/questions/20495/how-do-i-set-up-and-use-ffmpeg-in-windows)

**5. Setting up a Google/YouTube API (automatic uploading at the click of a button)**<br>
- [How to set up YouTube API](https://developers.google.com/youtube/v3/quickstart/python)

**6. Balabolka - Portable Version (Creates audio files from a text file)**<br>
- [Balabolka Download](http://www.cross-plus-a.com/bportable.htm)

**7. Selenium Headless Chrome (Will open the local reddit website replica in the background then add the text and take a screenshot of it)**<br>
- It is already installed so nothing needs to be done if you have Chrome version 76 downloaded
- Replace the application "chromedriver.exe" in the repository with the one suited for your version of chrome or download Chrome 76. **Newer versions of chrome might change how the HTML is displayed!**
[Chrome Driver Download](https://chromedriver.chromium.org/downloads)

**8. Local Reddit HTML replica (Screenshots will be taken from this)**<br>
- The HTML files in XAMPP directory so that they can be opened with Selenium on a local Apache web server <img src="https://i.imgur.com/bXe6J1F.png" width="90%" height="90%">



