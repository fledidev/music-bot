import youtube_dl
import logging

options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': './downloads/%(title)s.%(ext)s',
}


def download_video(video_url: str):
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_url])
        logging.debug(f"Downloading video: {video_url}")
