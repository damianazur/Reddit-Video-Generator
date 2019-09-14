# Reddit Video Maker

Automatically creates a narrated video of a Reddit topic, the question and replies to it are read out.<br>
It is like browsing Reddit but made into a video that can then be automatically uploaded to youtube.<br>
The program takes screenshots of the website in the background using headless chrome and using Balabolka <br>
gets the audio files which are combined into a video using FFMPEG. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
What things you need to install the software and how to install them

1. Python Libraries <br>
```
PIL: For automatically making thumbnails (editing images)
selenium: For opening a HTML file in the background, changing information in the local web page and taking screenshots
soundfile: For making sure the video/audio is of a certain length
praw: Reddit API for scaping/obtaining data from a subreddit/thread
shutil: For moving/copying files
pyperclip: Copying text to clipboard
win32con, win32api: Clicking on the screen
pynput: For using a virtual keyboard for automation
```
2. Reddit API application setup (Scrapes data from reddit)<br>
```
Sentdex has a great video on how to set it up:
[How to set up Reddit API Video](https://www.youtube.com/watch?v=NRgfgtzIhBQ/)
```
3. Local Reddit HTML replica (Screenshots will be taken off this)<br>
4. Selenium Headless Chrome (Will open the local reddit website replica in the background then add the text and take a screenshot of it)<br>
5. XAMPP Local Website Hosting - Apache (The local HTML file can be hosted using XAMPP so Headless Chrome can use it)<br>
```
https://www.apachefriends.org/index.html
```
6. FFMPEG Static Version (Combines image and audio files to make a video)<br>
```
https://ffmpeg.zeranoe.com/builds/
```
7. Setting up a Google/Youtube API (automatic uploading at the click of a button)<br>
```
https://developers.google.com/youtube/v3/quickstart/python
```
8. Balabolka - Portable Version (Creates audio files from a text file)<br>
```
http://www.cross-plus-a.com/bportable.htm
```


### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
