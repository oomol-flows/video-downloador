"""Format selector for video downloader"""

import re
from typing import Optional


def get_format_string(quality: str, audio_only: bool, hdr: bool = False, high_fps: bool = False, codec_preference: str = "h264", bitrate_limit: str = None) -> str:
    """Return the corresponding format string based on quality requirements"""
    if audio_only:
        return 'bestaudio[ext=m4a]/bestaudio/best'
    
    # Build format filters
    filters = []
    
    # Quality filters
    if quality == '4K' or quality == '2160p':
        filters.append('height<=2160')
    elif quality == '1440p':
        filters.append('height<=1440')
    elif quality == '1080p':
        filters.append('height<=1080')
    elif quality == '720p':
        filters.append('height<=720')
    elif quality == '480p':
        filters.append('height<=480')
    elif quality == '360p':
        filters.append('height<=360')
    elif quality == '240p':
        filters.append('height<=240')
    
    # HDR support
    if hdr:
        filters.append('dynamic_range=HDR10')
    
    # High frame rate support
    if high_fps:
        filters.append('fps>=50')
    
    # Codec preference
    if codec_preference == 'h265':
        filters.append('vcodec~="^((he|h\.?265|av01))')
    elif codec_preference == 'av1':
        filters.append('vcodec~="^av01"')
    elif codec_preference == 'vp9':
        filters.append('vcodec~="^vp9"')
    else:  # h264 default
        filters.append('vcodec~="^((avc|h\.?264))"')
    
    # Bitrate limit
    if bitrate_limit:
        try:
            bitrate_val = int(bitrate_limit.replace('k', '').replace('K', '').replace('m', '000').replace('M', '000'))
            filters.append(f'tbr<={bitrate_val}')
        except ValueError:
            pass  # Invalid bitrate format, ignore
    
    # Construct format string
    if filters:
        filter_str = '[' + ']['.join(filters) + ']'
        if quality == 'best':
            return f'bestvideo{filter_str}+bestaudio/best{filter_str}/best'
        else:
            return f'bestvideo{filter_str}+bestaudio/best{filter_str}/best'
    else:
        if quality == 'best':
            return 'bestvideo+bestaudio/best'
        else:
            quality_map = {
                '4K': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
                '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
                '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
                '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
                '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
                '240p': 'bestvideo[height<=240]+bestaudio/best[height<=240]',
            }
            return quality_map.get(quality, 'bestvideo+bestaudio/best')


def get_optimal_format_for_hd(info: dict, quality: str, hdr: bool = False, high_fps: bool = False, codec_preference: str = "h264") -> Optional[str]:
    """Get optimal format string based on available formats for HD video"""
    formats = info.get('formats', [])
    
    # Filter formats based on requirements
    suitable_formats = []
    
    for fmt in formats:
        height = fmt.get('height', 0)
        fps = fmt.get('fps', 0)
        vcodec = fmt.get('vcodec', '')
        dynamic_range = fmt.get('dynamic_range', '')
        
        # Check quality requirement
        if quality == '4K' and height < 2160:
            continue
        elif quality == '1440p' and height < 1440:
            continue
        elif quality == '1080p' and height < 1080:
            continue
        elif quality == '720p' and height < 720:
            continue
        
        # Check HDR requirement
        if hdr and 'HDR' not in dynamic_range:
            continue
        
        # Check high FPS requirement
        if high_fps and fps < 50:
            continue
        
        # Check codec preference
        if codec_preference == 'h265' and not re.search(r'(hevc|h265|x265)', vcodec, re.I):
            continue
        elif codec_preference == 'av1' and not re.search(r'av01', vcodec, re.I):
            continue
        elif codec_preference == 'vp9' and not re.search(r'vp9', vcodec, re.I):
            continue
        elif codec_preference == 'h264' and not re.search(r'(avc|h264|x264)', vcodec, re.I):
            continue
        
        suitable_formats.append(fmt)
    
    if suitable_formats:
        # Sort by quality (height, then bitrate)
        suitable_formats.sort(key=lambda x: (x.get('height', 0), x.get('tbr', 0)), reverse=True)
        best_format = suitable_formats[0]
        return f"{best_format['format_id']}+bestaudio"
    
    # Fallback to standard format selection
    return None