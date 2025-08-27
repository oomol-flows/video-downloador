"""File utilities for video downloader"""

import os
import glob
from pathlib import Path


def ensure_output_dir(output_dir: str) -> None:
    """Ensure output directory exists"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def find_downloaded_file(filename: str, output_dir: str, title: str, audio_only: bool = False, ext: str = None) -> str:
    """Find the actual downloaded file path"""
    # Check if the expected file exists
    if os.path.exists(filename):
        return filename
    
    # Try to find the actual downloaded file
    if not ext:
        ext = 'mp3' if audio_only else 'mp4'
    
    fallback_filename = os.path.join(output_dir, f"{title}.{ext}")
    
    # If still not found, use wildcard search
    if not os.path.exists(fallback_filename):
        pattern = os.path.join(output_dir, f"{title}*")
        files = glob.glob(pattern)
        if files:
            return max(files, key=os.path.getctime)
    
    return fallback_filename