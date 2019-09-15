# importing necessary libraries 
import os 
import urllib.request, urllib.parse, urllib.error 
import http.client 
import urllib.request 
import urllib.error 
import http.client 
import httplib2 
import random 
import time
import datetime
import google.oauth2.credentials 
import google_auth_oauthlib.flow 
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError 
from google_auth_oauthlib.flow import InstalledAppFlow 
from apiclient.http import MediaFileUpload
import dateutil.parser as dp

THIS_FILE_PATH = os.getcwd()
os.chdir('..')
REPO_PATH = os.getcwd() + "\\" 
os.chdir(THIS_FILE_PATH)

# The CLIENT_SECRETS_FILE variable 
# specifies the name of a file that 
# contains client_id and client_secret. 
CLIENT_SECRETS_FILE = REPO_PATH + "JSON Files\\client1.json"

# This scope allows for full read / 
# write access to the authenticated 
# user's account and requires requests 
# to use an SSL connection. 
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl'] 
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    print("get_authenticated_service")
    flow = InstalledAppFlow.from_client_secrets_file( 
                                            CLIENT_SECRETS_FILE, SCOPES) 
                                            
    credentials = flow.run_console() 
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials) 


# Here we are telling HTTP Transport 
# Library not to retry the video upload. 
httplib2.RETRIES = 1

# MAX_RETRIES specifies the maximum number 
# of retries that can done before giving up. 
MAX_RETRIES = 10

# Always retry when these exceptions are raised. 
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, 
						http.client.NotConnected, 
						http.client.IncompleteRead, 
						http.client.ImproperConnectionState, 
						http.client.CannotSendRequest, 
						http.client.CannotSendHeader, 
						http.client.ResponseNotReady, 
						http.client.BadStatusLine) 

# Always retry when an apiclient.errors.HttpError 
# with one of these status codes is raised. 
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

LATEST_VIDEO_ID = 0

# This method implements an exponential 
# backoff strategy to resume a failed upload. 
def resumable_upload(request, resource, method):
    print("resumable_upload")
    response = None
    error = None
    retry = 0

    while response is None: 
        try:     
            print("Uploading the file...") 
            status, response = request.next_chunk() 
                
            if response is not None:            
                if method == 'insert' and 'id' in response:
                    print("Upload successful:", )
                    print(response)
                    print("\n\n\n id:", response["id"])
                    global LATEST_VIDEO_ID
                    LATEST_VIDEO_ID = response["id"]
                    
                elif method != 'insert' or 'id' not in response:
                    print("Upload not successful")
                    print(response) 
                else:
                    print("Upload not successful: Unknown")
                    exit("The file upload failed with an unexpected response: % s" % response) 
                            
        except HttpError as e: 
            if e.resp.status in RETRIABLE_STATUS_CODES: 
                error = "A retriable HTTP error % d occurred:\n % s" % (e.resp.status, e.content) 
            else: 
                raise
            
        except RETRIABLE_EXCEPTIONS as e: 
            error = "A retriable error occurred: % s" % e 

            if error is not None: 
                print(error) 
            retry += 1
                
            if retry > MAX_RETRIES: 
                exit("No longer attempting to retry.") 

            max_sleep = 2 ** retry 
            sleep_seconds = random.random() * max_sleep 
      
            print(("Sleeping % f seconds and then retrying..." % sleep_seconds)) 
            time.sleep(sleep_seconds)


def setThumbnail(videoID, thumbnailFilePath, client):
    print("Uploading Thumbanil")
    request = client.thumbnails().set(
        videoId=videoID,
        
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(thumbnailFilePath)
    )
    response = request.execute()
    print(response)

                
def print_response(response):
        print("printing response:\n\n")
        print(response)


# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
    print("properties", properties)

    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]
            # Convert a name like "snippet.tags[]" to snippet.tags, but handle
            # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key)-2:]
                is_array = True
            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.      
                if properties[p]:
                    if is_array:
                        print("if properties[p]", properties[p].split(','))
                        ref[key] = properties[p].split(',')
                    else:
                        print("else properties[p]", properties[p])
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
                # For example, the property is "snippet.description", and the resource
                # already has a "snippet" object.
                print("else:", ref[key])
                ref = ref[key]

    print("\n\n", resource)
    return resource 


# Remove keyword arguments that are not set 
def remove_empty_kwargs(**kwargs):
    print("remove_empty_kwargs")
    good_kwargs = {}
	
    if kwargs is not None: 
            for key, value in list(kwargs.items()): 
                if value:
                    good_kwargs[key] = value
    return good_kwargs 


def videos_insert(client, properties, media_file, **kwargs):
    print("videos_insert")
    resource = build_resource(properties) 
    kwargs = remove_empty_kwargs(**kwargs)
    
    request = client.videos().insert(body = resource, 
        media_body = MediaFileUpload(media_file, 
        chunksize =-1, resumable = True), **kwargs) 
	
    return resumable_upload(request, 'video', 'insert') 


def queueScheduleTimes():
    txtFilePath = REPO_PATH + "TXTFiles\\ScheduleTimesQueue.txt"
    increment = 6 #hours
    currentHours = 0
    
    i = 0
    f = open(txtFilePath, "a+")
    startTime = "2019-08-18T16:50:00.000+00:00"

    while i < 10000:
        currentHours += increment
        converted_ticks = datetime.datetime.now() + datetime.timedelta(currentHours/24)
        f.write(converted_ticks.strftime("%Y-%m-%dT%H:00:00.000+00:00") + "\n")

        i += 1

    f.close()


def iso8601ToSec(t):
    #t = '2019-08-19T01:00:00.000+00:00'
    parsed_t = dp.parse(t)
    t_in_seconds = parsed_t.timestamp()
    #print(t_in_seconds, time.time(), "difference:", time.time() - t_in_seconds)
    
    return t_in_seconds


def getScheduleTime():
    amount = 1
    with open(REPO_PATH + "TXTFiles\\ScheduleTimesQueue.txt", 'r') as fin:
        data = fin.read().splitlines(True)

    i = 0
    isoTime = data[i]
    #print(isoTime)
    time_in_sec = iso8601ToSec(isoTime)
    difference = time_in_sec - time.time()
    #print(difference)
    while difference < 600:
        amount += 1
        i += 1
        isoTime = data[i]
        time_in_sec = iso8601ToSec(isoTime)
        difference = time_in_sec - time.time()
        
    #with open("C:\\Users\\User1\\Desktop\\Talk Reddit\\VideoMakerRepo\\ScheduleTimesQueue.txt", 'w') as fout:
    #    fout.writelines(data[amount:])
    print(i, data[i])
    return str(data[i])


def removeScheduleTime(timeToRemove):
    #print("Removing:", timeToRemove)
    with open(REPO_PATH + "TXTFiles\\ScheduleTimesQueue.txt", 'r') as fin:
        data = fin.read().splitlines(True)

    index = data.index(timeToRemove)
    arraySize = len(data)
    #print("Index = ", index)
    with open(REPO_PATH + "TXTFiles\\ScheduleTimesQueue.txt", 'w') as fout:
        fout.writelines(data[index + 1:])


# Deletes the first line from the file
def firstLineDel(filePath):
    with open(filePath, 'r') as fin:
        data = fin.read().splitlines(True)
        
    with open(filePath, 'w') as fout:
        fout.writelines(data[1:])


def fileToDictionary(filePath, keyType):
    d = {}
    index = 0
    f = open(filePath, 'r')
    for line in f:
        lineDict = {}
        variables = line.strip().split(";")
        for var in variables:
            k, v = var.strip().split(' = ')

            if keyType == "byLineNumber":
                lineDict[k.strip()] = v.strip()
            else:
                d[k.strip()] = v.strip()

        if keyType == "byLineNumber":
            d[index] = lineDict
            index += 1

    f.close()
    return d


def uploadMainFunction(properties):
    print("Starting uploadMainFunction")
    title = properties["title"]
    description = properties["description"]
    tags = properties["tags"]
    privacyStatus = properties["privacyStatus"]
    categoryId = properties["categoryId"]
    defaultLanguage = properties["defaultLanguage"]
    videoFilePath = properties["videoFilePath"]
    thumbnailPath = properties["thumbnailPath"]
    videoUploadVars = properties["videoUploadVars"]

    title = "[#" + str(videoUploadVars["thumbnailIndex"]) + "] " + title
    variablesFilePath = REPO_PATH + "TXTFiles\\Variables.txt"
    
    # When running locally, disable OAuthlib's 
    # HTTPs verification. When running in production 
    # * do not * leave this option enabled. 
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    global CLIENT
    try:
        CLIENT
    except NameError:
          CLIENT = get_authenticated_service()
    
    client = CLIENT
    media_file = videoFilePath
    if not os.path.exists(media_file): 
        exit('Please specify the complete valid file location.')

    scheduleTime = getScheduleTime()
    cleanedScheduleTime = scheduleTime.rstrip()
    print("Schedule Time:", scheduleTime)
    print("Title:", title)
    print("Descripton:", description)

    exceptionOccured = False
    try: 
        videos_insert(client, 
            {'snippet.categoryId': categoryId, 
            'snippet.defaultLanguage': defaultLanguage, 
            'snippet.description': description,
            'snippet.tags[]': tags, 
            'snippet.title': title,
            'status.embeddable': '',
            'status.license': '',
            'status.privacyStatus': privacyStatus,
            'status.publishAt': cleanedScheduleTime,
            'status.publicStatsViewable': ''}, 
            media_file,
            part = 'snippet, status')
    except Exception as e:
        exceptionOccured = True
        print(e)

    if exceptionOccured == False:
        videoUploadVars["thumbnailIndex"] = str(int(videoUploadVars["thumbnailIndex"]) + 1)
        dictToFile(variablesFilePath, videoUploadVars)
        firstLineDel(REPO_PATH + "TXTFiles\\ScheduleVideosQueue.txt")
            
        time.sleep(10)

        removeScheduleTime(scheduleTime)
        setThumbnail(LATEST_VIDEO_ID, thumbnailPath, client)


def dictToFile(filePath, dictionary):
    f = open(filePath, 'w')
    for key in dictionary.keys():
        lineToWrite = key + " = " + str(dictionary[key]) + "\n"
        f.write(lineToWrite)
        
    f.close()


def getUploadProperties():
    print("Getting Upload Properties")
    # Get variables from file into a dictionary
    variablesFilePath = REPO_PATH + "TXTFiles\\Variables.txt"
    videoUploadVars = fileToDictionary(variablesFilePath, "")
    thumbnailIndex = videoUploadVars["thumbnailIndex"]

    queuedVideoVars = fileToDictionary(REPO_PATH + "TXTFiles\\ScheduleVideosQueue.txt", "byLineNumber")
        
    threadID = queuedVideoVars[0]["threadID"]
    videoTitle = queuedVideoVars[0]["title"]

    description = ("Do you think they are the asshole?\n"
                    "Comment below!\n\n"

                    "ATA - You're The Asshole\n"
                    "NTA - Not The Asshole\n"
                    "INFO - Not Enough Info\n"
                    "ESH - Everyone Sucks Here\n"
                    "NAH - No A-holes here")

    tags = "reddit, r/story, #reddit, r/AITA, r/AmITheAsshole, Am I The Asshole?"
    print(thumbnailIndex)
    print(videoTitle)
    print(threadID)
        
    properties = {"title"           :videoTitle,
                  "description"     :description,
                  "tags"            :tags,
                  "privacyStatus"   :"private",
                  "categoryId"      :"24",
                  "defaultLanguage" :"",
                  "videoFilePath"   :REPO_PATH + "Videos\\" + threadID + "\\CompleteVideo.mp4",
                  "thumbnailPath"   :REPO_PATH + "Images\\Thumbnails\\" + thumbnailIndex + ".jpg",
                  "videoUploadVars" :videoUploadVars
                 }

    return properties


