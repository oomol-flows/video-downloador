"""Info handler for video downloader"""

from oocana import Context
from ..utils.format_utils import format_duration, format_view_count
from ..formatters.quality_analyzer import analyze_available_formats, get_format_features_info


def display_video_info(info: dict, context: Context) -> None:
    """Display video information to user"""
    title = info.get('title', 'Unknown')
    duration = info.get('duration', 0)
    uploader = info.get('uploader', 'Unknown')
    view_count = info.get('view_count', 0)
    
    # Format duration and view count
    duration_str = format_duration(duration)
    view_str = format_view_count(view_count)
    
    print(f'📺 Title: {title}\n👤 Uploader: {uploader}\n⏱️ Duration: {duration_str}\n👁️ Views: {view_str}')
    
    # Analyze and display available formats
    formats = info.get('formats', [])
    available_qualities, hdr_available, high_fps_available = analyze_available_formats(formats)
    
    features = get_format_features_info(available_qualities, hdr_available, high_fps_available)
    
    if features:
        print(f'🎬 {" | ".join(features)}')


def prepare_video_info(info: dict) -> dict:
    """Prepare video information for output"""
    return {
        'title': info.get('title', ''),
        'duration': info.get('duration', 0),
        'uploader': info.get('uploader', ''),
        'view_count': info.get('view_count', 0),
        'upload_date': info.get('upload_date', ''),
        'webpage_url': info.get('webpage_url', ''),
        'thumbnail': info.get('thumbnail', ''),
    }


def display_download_info(quality: str, hdr: bool, high_fps: bool, codec_preference: str, context: Context) -> None:
    """Display download start information"""
    download_info = f'🚀 Starting download\n📺 Quality: {quality}'
    if hdr:
        download_info += ' (HDR)'
    if high_fps:
        download_info += ' (High FPS)'
    download_info += f'\n🎥 Codec: {codec_preference.upper()}'
    
    print(download_info)