"""Progress handler for video downloader"""

import os
from oocana import Context
from ..utils.format_utils import format_file_size


def create_progress_hook(context: Context):
    """Create a progress hook function for yt-dlp"""
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            total_bytes = d.get('total_bytes', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            # Format file size
            size_info = format_file_size(total_bytes, downloaded_bytes)
            
            print(f'Progress: {percent} - {size_info} - Speed: {speed} - ETA: {eta}')
            context.preview({
                'type': 'text',
                'data': f'📥 Downloading: {percent}\n📊 Size: {size_info}\n🚀 Speed: {speed}\n⏱️ ETA: {eta}'
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