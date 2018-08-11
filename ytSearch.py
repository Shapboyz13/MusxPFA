#!/usr/bin/python

from apiclient.discovery import build


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBsQOXjf7saEoDpouxQF9mbHwNu7Ap0IIY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options,
        part="id,snippet",
        maxResults=5,
    ).execute()

    data=[]
    for x in search_response.get("items"):
        data.append({
            'videoId'       : x['id']['videoId'],
            'channelTitle'  : x['snippet']['channelTitle'],
            'title'         : x['snippet']['title'],
            'img'           : x['snippet']['thumbnails']['high']['url']  if x['snippet']['thumbnails']['high']['url'] else x['snippet']['thumbnails']['default']['url']
        })
    return data
