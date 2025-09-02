"""Progress handler for video downloader"""

import os
from oocana import Context
from ..utils.format_utils import format_file_size


def parse_percent_str(percent_str: str) -> int:
    """Convert percentage string like '100.0%' to integer 1-100"""
    if not percent_str or percent_str == 'N/A':
        return 0
    try:
        # Remove % sign and convert to float
        percent_value = float(percent_str.rstrip('%'))
        # Ensure it's within 0-100 range and convert to int
        return max(0, min(100, int(round(percent_value))))
    except (ValueError, AttributeError):
        return 0


def create_progress_hook(context: Context):
    """Create a progress hook function for yt-dlp"""
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            # Convert percent string to number
            percent_num = parse_percent_str(percent_str)
            
            # Format file size
            size_info = format_file_size(total_bytes, downloaded_bytes)
            context.report_progress(percent_num)
            print(f'Progress: {percent_num}% - {size_info} - Speed: {speed} - ETA: {eta}')
            context.preview({
                'type': 'text',
                'data': f'📥 Downloading: {percent_num}%\n📊 Size: {size_info}\n🚀 Speed: {speed}\n⏱️ ETA: {eta}'
            })
        elif d['status'] == 'finished':
            filename = d.get('filename', 'Unknown file')
            context.preview({
                'type': 'text',
                'data': f'✅ Download completed: {os.path.basename(filename)}'
            })
        elif d['status'] == 'error':
            context.preview({
                'type': 'text',
                'data': f'❌ Download error occurred'
            })
    
    return progress_hook