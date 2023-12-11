import os

import youtube_dl
import logging
import json
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey='KEY')

options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': './downloads/%(title)s.%(ext)s',
}


def download_video(video_url: str):
    with youtube_dl.YoutubeDL(options) as ydl:
        video_info = ydl.extract_info(video_url)
        download_name = ydl.prepare_filename(video_info)
        ydl.download([video_url])
        logging.debug(f"Downloading video: {video_url}")
        create_meta(video_info['title'], video_info['uploader'], video_info['thumbnail'], download_name, video_info['duration'])
        return download_name


def create_meta(title: str, author: str, thumbnail_path: str, music_path: str, music_duration: int):
    meta = {
        "music_source": music_path,
        "music_duration": music_duration,
        "title": title,
        "thumbnail_source": thumbnail_path,
        "author": author
    }

    json_object = json.dumps(meta, indent=4)

    with open(f"metadata/{title}.json", "w") as file:
        file.write(json_object)


def youtube_search(query: str):
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
    ).execute()

    videos = []

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'videoId': search_result['id']['videoId']
            })

    return videos
