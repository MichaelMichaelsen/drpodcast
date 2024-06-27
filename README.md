# drpodcast
## Introduction
This is a tool when you need to be able to listen to DR podcasts offline. 
The idea is to be able to download the podcasts as mp3 files and then use them offline.

## Overview
A Python script to download podcast from dr.dk

## Description
This script will parse the RSS link from dr.com and download the podcast as mp3 files.
Go to https://www.dr.dk/lyd/programmer to find a podcast,
then copy link from the RSS feed and use this as argument --url for the script.
The script will create a directory with the name of the podcast serie and add all the mp3 file in that directory.
The mp3 will be prefixed with the date of the publication.

## Installation

### Prerequisite

Ensure that all the needed Python packages are installed

```
pip install -r requirements.txt
```

### Install

Clone the repo

## Usage
```
python drpodcast.py --url https://api.dr.dk/podcasts/v1/feeds/tabloid-3
```

### Url from DR podcasts
This can be extracted in the overview page for each podcast.
<img src="images/RSSIcon.png" alt="RSSIcon">
 On the RSS icon, just right click, select copy link and use that link as argument for the script.

### DR podcast
Currently I have found the following podcasts

* https://api.dr.dk/podcasts/v1/feeds/stjerner-og-striber-podcast
* https://api.dr.dk/podcasts/v1/feeds/prompt
* https://api.dr.dk/podcasts/v1/feeds/guld-og-groenne-skove
* https://api.dr.dk/podcasts/v1/feeds/djaevlen-i-detaljen
* https://api.dr.dk/podcasts/v1/feeds/tabloid-3
* https://api.dr.dk/podcasts/v1/feeds/foelg-pengene
* https://api.dr.dk/podcasts/v1/feeds/kampen-om-historien-3
* https://api.dr.dk/podcasts/v1/feeds/genstart
