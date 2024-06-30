#
# drpotcast will decode the RSS xml file and extract the mp3 part of the file
#
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET
import requests
from pathvalidate import sanitize_filename
import yt_dlp

VERSION = "0.0.3"
HELP_TEXT = "URL for the RSS feed."
DESCRIPTION = """
This script will parse the RSS link from dr.com and download the podcast as mp3 files.
Go to https://www.dr.dk/lyd/programmer to find a podcast,
then copy link from the RSS feed and use this as argument --url for the script.
The script will create a directory with the name of the podcast serie and add all the mp3 file in that directory.
The mp3 will be prefixed with the date of the publication.

Example

   python drpodcast.py --url https://api.dr.dk/podcasts/v1/feeds/kampen-om-historien-3

Will create a directory "Kampen om historien" and add the downloaded mp3 files.
"""

def download_rss_xml_file(rssurl: str) -> str:
    """
    Download the RSS xml with a given url
    """
    try:
        response = requests.get(rssurl)
        response.raise_for_status()
        htmltext = response.text
        return htmltext
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error. {errh.args[0]}")
        return None
    except requests.exceptions.ReadTimeout as errrt:
        print(f"Time out. Error code {errrt}")
        return None
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error. Error code {conerr}")
        return None

def make_episode_list( htmltext: str)-> list:
    """
    Parse the rss xml file and extract a list of episoder (item).
    """
    podcast_list = []
    root = ET.fromstring(htmltext)
    for idx, item in enumerate(root.findall('.//item')):
        title = item.find('title')
        title_text = title.text
        podcast_list.append(title_text)
    return podcast_list

def main(rssurl:str):
    """
    Main control
    """
    htmltext = download_rss_xml_file(rssurl)
    episode_list = make_episode_list(htmltext=htmltext)
    print(f"{len(episode_list)} episoder:")
    for episode in episode_list:
        print(episode)
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
            # Ensure that we do not have strange characters in the file name
            title_clean = sanitize_filename(title_text)
            output_template = f"{date_only} {title_clean}.%(ext)s"
            yt_opts = {
                'verbose': False,
                'outtmpl': output_template,
                'windows-filenames': True,
                'socket_timeout': 10,
                'paths': {'home': download_path}
            }
            podcast_url = enclosure.get('url')
            with yt_dlp.YoutubeDL(yt_opts) as ydl:
                ydl.download(podcast_url)
            print('-' * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--url', type=str,
                        default="https://api.dr.dk/podcasts/v1/feeds/kampen-om-historien-3", help=HELP_TEXT)
    args = parser.parse_args()
    url = args.url
    main(url)
