"""File utilities for video downloader"""

import os
import glob
import re
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """Remove or replace characters that are invalid in Windows filenames"""
    # Windows forbidden characters: < > : " / \ | ? *
    # Also remove control characters (ASCII 0-31)
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    sanitized = re.sub(invalid_chars, '_', filename)

    # Remove trailing dots and spaces (not allowed in Windows)
    sanitized = sanitized.rstrip('. ')

    # Ensure filename is not empty
    if not sanitized:
        sanitized = 'video'

    return sanitized


def ensure_output_dir(output_dir: str) -> None:
    """Ensure output directory exists"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)


def find_downloaded_file(filename: str, output_dir: str, title: str, audio_only: bool = False, ext: str = None) -> str:
    """Find the actual downloaded file path"""
    # Check if the expected file exists
    if os.path.exists(filename):
        return os.path.abspath(filename)

    # Sanitize title for safe filename
    safe_title = sanitize_filename(title)

    # Try to find the actual downloaded file
    if not ext:
        ext = 'mp3' if audio_only else 'mp4'

    # Use Path for cross-platform compatibility
    output_path = Path(output_dir)
    fallback_filename = output_path / f"{safe_title}.{ext}"

    # If still not found, use wildcard search
    if not fallback_filename.exists():
        pattern = str(output_path / f"{safe_title}*")
        files = glob.glob(pattern)
        if files:
            # Return the most recently created file
            return os.path.abspath(max(files, key=os.path.getctime))

    return str(fallback_filename.absolute())