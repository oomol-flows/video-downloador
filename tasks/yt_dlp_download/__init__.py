# region generated meta
import typing

class Inputs(typing.TypedDict):
    url: str
    format: typing.Optional[str]
    output_dir: typing.Optional[str]
    filename_template: typing.Optional[str]
    quality: typing.Optional[str]
    audio_only: typing.Optional[bool]
    subtitle_langs: typing.Optional[str]
    proxy: typing.Optional[str]

class Outputs(typing.TypedDict):
    video_path: str
    info: dict

# endregion

import os
import json
import yt_dlp
from oocana import Context
from pathlib import Path

def main(params: Inputs, context: Context) -> Outputs:
    """
    Download videos using yt-dlp
    
    Args:
        params: Input parameters
        context: OOMOL context
        
    Returns:
        Dictionary containing video path and information
    """
    
    url = params["url"]
    output_dir = params.get("output_dir")
    format_spec = params.get("format", "best")
    filename_template = params.get("filename_template")
    quality = params.get("quality", "best")
    audio_only = params.get("audio_only", False)
    subtitle_langs = params.get("subtitle_langs")
    proxy = params.get("proxy")
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Set default filename template
    if not filename_template:
        filename_template = "%(title)s.%(ext)s"
    
    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, filename_template),
        'format': format_spec if format_spec != "best" else get_format_string(quality, audio_only),
    }
    
    # Download audio only
    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    # Subtitle download
    if subtitle_langs:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = subtitle_langs.split(',')
        ydl_opts['writeautomaticsub'] = True
    
    # Proxy settings
    if proxy:
        ydl_opts['proxy'] = proxy
    
    # Progress callback
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(percent)
            context.preview({
                'type': 'text',
                'data': f'Download progress: {percent} Speed: {speed} ETA: {eta}'
            })
        elif d['status'] == 'finished':
            context.preview({
                'type': 'text',
                'data': f'Download completed: {d["filename"]}'
            })
    
    ydl_opts['progress_hooks'] = [progress_hook]
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video information
            info = ydl.extract_info(url, download=False)
            
            # Start download
            ydl.download([url])
            
            # Get actual downloaded file path
            filename = ydl.prepare_filename(info)
            if audio_only:
                # If audio only, extension will become .mp3
                base_name = os.path.splitext(filename)[0]
                filename = base_name + '.mp3'
            
            # Ensure file exists
            if not os.path.exists(filename):
                # Try to find the actual downloaded file
                title = info.get('title', 'video')
                ext = 'mp3' if audio_only else info.get('ext', 'mp4')
                filename = os.path.join(output_dir, f"{title}.{ext}")
                
                # If still not found, use wildcard search
                if not os.path.exists(filename):
                    import glob
                    pattern = os.path.join(output_dir, f"{title}*")
                    files = glob.glob(pattern)
                    if files:
                        filename = max(files, key=os.path.getctime)
            
            # Prepare output information
            video_info = {
                'title': info.get('title', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', ''),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'webpage_url': info.get('webpage_url', ''),
                'thumbnail': info.get('thumbnail', ''),
            }
            
            return {
                'video_path': filename,
                'info': video_info
            }
            
    except Exception as e:
        context.preview({
            'type': 'text',
            'data': f'Download failed: {str(e)}'
        })
        raise Exception(f"Video download failed: {str(e)}")

def get_format_string(quality: str, audio_only: bool) -> str:
    """Return the corresponding format string based on quality requirements"""
    if audio_only:
        return 'bestaudio/best'
    
    quality_map = {
        'best': 'best',
        '1080p': 'best[height<=1080]',
        '720p': 'best[height<=720]',
        '480p': 'best[height<=480]',
        '360p': 'best[height<=360]',
    }
    
    return quality_map.get(quality, 'best')