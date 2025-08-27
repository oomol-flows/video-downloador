"""Quality analyzer for video formats"""

from typing import Dict, Set, Tuple


def analyze_available_formats(formats: list) -> Tuple[Set[str], bool, bool]:
    """Analyze available formats and return quality info
    
    Returns:
        Tuple of (available_qualities, hdr_available, high_fps_available)
    """
    available_qualities = set()
    hdr_available = False
    high_fps_available = False
    
    for fmt in formats:
        height = fmt.get('height')
        fps = fmt.get('fps', 0)
        dynamic_range = fmt.get('dynamic_range', '')
        
        if height:
            if height >= 2160:
                available_qualities.add('4K')
            elif height >= 1440:
                available_qualities.add('1440p')
            elif height >= 1080:
                available_qualities.add('1080p')
            elif height >= 720:
                available_qualities.add('720p')
        
        if dynamic_range and 'HDR' in dynamic_range:
            hdr_available = True
        
        if fps and fps >= 50:
            high_fps_available = True
    
    return available_qualities, hdr_available, high_fps_available


def get_format_features_info(available_qualities: Set[str], hdr_available: bool, high_fps_available: bool) -> list:
    """Get formatted features information"""
    features = []
    if available_qualities:
        features.append(f"Qualities: {', '.join(sorted(available_qualities, reverse=True))}")
    if hdr_available:
        features.append("HDR available")
    if high_fps_available:
        features.append("High FPS available")
    
    return features