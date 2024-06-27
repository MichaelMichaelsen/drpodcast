#
# drpotcast will decode the RSS xml file and extract the mp3 part of the file
#
import argparse
import requests
import xml.etree.ElementTree as ET
import os
import subprocess
from datetime import datetime

parser = argparse.ArgumentParser(description='Parse rss xml file and download DR podcasts')
parser.add_argument('--url', type=str, 
                    default="https://api.dr.dk/podcasts/v1/feeds/stjerner-og-striber-podcast", help="URL for the RSS feed")
args = parser.parse_args()
url = args.url
response = requests.get(url)
if response.status_code == 200:
    htmltext = response.text
    root = ET.fromstring(htmltext)
    # Extract the subdirectory name from the image title
    podcast_title = root.find('.//channel/title').text
    print(f"Podcast title {podcast_title}")
    directory_name = podcast_title
    # Create a sub directory with the podcast title
    try:
        os.mkdir(directory_name)    
    except FileExistsError:
        pass
    # Parse the xml and find all the titles and the url
    #file_name = "files.sh"
    #outputfile = os.path.join(directory_name, file_name)
    #outputfh = open(outputfile, "w")
    os.chdir(directory_name)
    for idx, item in enumerate(root.findall('.//item')):
        title = item.find('title')
        # Skip all teaser
        title_text = title.text
        if title_text.find('Teaser') == -1:
            enclosure = item.find('enclosure')
            # Extract the date from the timestampe and use as prefix in the filename
            pubdate = item.find('pubDate').text
            date_object = datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')
            date_only = date_object.strftime('%Y-%m-%d')
            output_file = date_only + ' ' + title_text + ".mp3"
            url = enclosure.get('url')
            #print(f'yt-dlp --restrict-filenames -o "{output_file}" {url}', file=outputfh)
            
            args = ["yt-dlp", "--restrict-filenames", "-o", output_file, url ]
            result = subprocess.run(args, shell=False, text=True)
            print(result)
            print('-' * 50)
    #print(f"Output file {file_name} created.")