"""yt-dlp configuration module"""

import os
from typing import Dict, Any, Optional


def create_ydl_options(output_dir: str, filename_template: str, format_spec: str, proxy: Optional[str] = None) -> Dict[str, Any]:
    """Create base yt-dlp options"""
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, filename_template),
        'format': format_spec,
        'merge_output_format': 'mp4',  # Ensure compatibility
        'writeinfojson': True,  # Save video info
        'writethumbnail': True,  # Save thumbnail
        'ignoreerrors': False,  # Stop on errors
        'no_warnings': False,  # Show warnings
        'extractaudio': False,  # Don't extract audio by default
        'audioformat': 'best',  # Best audio format
        'embed_subs': True,  # Embed subtitles if available
        'writesubtitles': False,  # Don't write separate subtitle files by default
        'writeautomaticsub': False,  # Don't write auto-generated subtitles by default
    }
    
    # Proxy settings
    if proxy:
        ydl_opts['proxy'] = proxy
    
    return ydl_opts


def configure_audio_options(ydl_opts: Dict[str, Any], audio_only: bool) -> Dict[str, Any]:
    """Configure audio-specific options"""
    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    return ydl_opts


def configure_subtitle_options(ydl_opts: Dict[str, Any], subtitle_langs: Optional[str]) -> Dict[str, Any]:
    """Configure subtitle options"""
    if subtitle_langs:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = subtitle_langs.split(',')
        ydl_opts['writeautomaticsub'] = True
    
    return ydl_opts


def get_default_filename_template() -> str:
    """Get default filename template"""
    return "%(title)s.%(ext)s"