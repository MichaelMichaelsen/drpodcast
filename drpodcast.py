#
# drpotcast will decode the RSS xml file and extract the mp3 part of the file
#
import argparse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pathvalidate import sanitize_filename
import yt_dlp

version = "0.0.3"

help_text = "URL for the RSS feed."
description = """
This script will parse the RSS link from dr.com and download the podcast as mp3 files.
Go to https://www.dr.dk/lyd/programmer to find a podcast,
then copy link from the RSS feed and use this as argument --url for the script.
The script will create a directory with the name of the podcast serie and add all the mp3 file in that directory.
The mp3 will be prefixed with the date of the publication.

Example

   python drpodcast.py --url https://api.dr.dk/podcasts/v1/feeds/kampen-om-historien-3

Will create a directory "Stjerner og striber" and add the downloaded mp3 files.
"""

parser = argparse.ArgumentParser(description=description,formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--url', type=str, 
                    default="https://api.dr.dk/podcasts/v1/feeds/kampen-om-historien-3", help=help_text)
args = parser.parse_args()
url = args.url
try:
    response = requests.get(url)
    response.raise_for_status()
    htmltext = response.text
    root = ET.fromstring(htmltext)
    # Extract the subdirectory name from the image title
    podcast_title = root.find('.//channel/title').text
    print(f"Podcast title {podcast_title}")
    download_path = f"./podcasts/{podcast_title}"
    # Parse the xml and find all the titles and the url
    for idx, item in enumerate(root.findall('.//item')):
        title = item.find('title')
        title_text = title.text
        # Skip all teaser
        if title_text.find('Teaser') == -1:
            enclosure = item.find('enclosure')
            # Extract the date from the timestampe and use as prefix in the filename
            pubdate = item.find('pubDate').text
            date_object = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')
            date_only = date_object.strftime('%Y-%m-%d')
            title_clean = sanitize_filename(title_text) # Ensure that we do not have strange characters in the file name
            output_template = f"{date_only} {title_clean}.%(ext)s"
            yt_opts = {
               'verbose': False,
                'outtmpl': output_template,
                'windows-filenames': True,
                #'simulate': True,
                'paths': {'home': download_path}
            }
            # args = ["yt-dlp", "--restrict-filenames", "-o", output_file, url ]
            # result = subprocess.run(args, shell=False, text=True)
            # print(result)
            url = enclosure.get('url')
            with yt_dlp.YoutubeDL(yt_opts) as ydl:
                ydl.download(url)
            print('-' * 50)
    #print(f"Output file {file_name} created.")
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error. {errh.args[0]}")
except requests.exceptions.ReadTimeout as errrt: 
    print("Time out")
except requests.exceptions.ConnectionError as conerr: 
    print("Connection error") 