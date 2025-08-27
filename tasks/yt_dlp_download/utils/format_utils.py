"""Format utilities for video downloader"""


def format_duration(duration: int) -> str:
    """Format duration in seconds to HH:MM:SS or MM:SS format"""
    if duration <= 0:
        return 'Unknown'
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        return f'{minutes:02d}:{seconds:02d}'


def format_view_count(view_count: int) -> str:
    """Format view count to human readable format"""
    if view_count <= 0:
        return 'Unknown views'
    
    if view_count >= 1000000:
        return f'{view_count/1000000:.1f}M views'
    elif view_count >= 1000:
        return f'{view_count/1000:.1f}K views'
    else:
        return f'{view_count} views'


def format_file_size(total_bytes: int, downloaded_bytes: int) -> str:
    """Format file size to MB format"""
    if total_bytes > 0:
        size_mb = total_bytes / (1024 * 1024)
        downloaded_mb = downloaded_bytes / (1024 * 1024)
        return f'{downloaded_mb:.1f}MB / {size_mb:.1f}MB'
    else:
        return 'Unknown size'