"""yt-dlp configuration module"""

import os
from pathlib import Path
from typing import Dict, Any, Optional


def create_ydl_options(output_dir: str, filename_template: str, format_spec: str, proxy: Optional[str] = None, cookies_file: Optional[str] = None) -> Dict[str, Any]:
    """Create base yt-dlp options"""
    # Use Path for cross-platform compatibility
    output_path = Path(output_dir) / filename_template

    ydl_opts = {
        'outtmpl': str(output_path),
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
        # Anti-bot protection headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
        # Network settings to handle throttling and errors
        'retries': 10,  # Retry on network errors
        'fragment_retries': 10,  # Retry on fragment download errors
        'file_access_retries': 3,  # Retry on file access errors
        'extractor_retries': 3,  # Retry on extractor errors
        'sleep_interval': 1,  # Sleep between requests (anti-throttling)
        'max_sleep_interval': 5,  # Max sleep time
        'nocheckcertificate': False,  # Verify SSL certificates for security
    }

    # Proxy settings
    if proxy:
        ydl_opts['proxy'] = proxy

    # Cookie settings
    if cookies_file:
        cookie_path = Path(cookies_file)
        if cookie_path.is_file():
            ydl_opts['cookiefile'] = str(cookie_path)

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