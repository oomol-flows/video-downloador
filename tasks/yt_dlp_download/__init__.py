# region generated meta
import typing

class Inputs(typing.TypedDict):
    url: str
    format: typing.Optional[str]
    output_dir: typing.Optional[str]
    filename_template: typing.Optional[str]
    quality: typing.Optional[str]
    audio_only: typing.Optional[bool]
    subtitle_langs: typing.Optional[str]
    proxy: typing.Optional[str]
    hdr: typing.Optional[bool]
    high_fps: typing.Optional[bool]
    codec_preference: typing.Optional[str]
    bitrate_limit: typing.Optional[str]
    cookies_file: typing.Optional[str]

class Outputs(typing.TypedDict):
    video_path: str
    info: dict

# endregion

import os
import yt_dlp
from oocana import Context

# Import modular components
from .utils import ensure_output_dir, find_downloaded_file
from .formatters import get_format_string, get_optimal_format_for_hd
from .handlers import create_progress_hook, display_video_info, prepare_video_info, display_download_info
from .config import create_ydl_options, configure_audio_options, configure_subtitle_options, get_default_filename_template

def main(params: Inputs, context: Context) -> Outputs:
    """
    Download videos using yt-dlp
    
    Args:
        params: Input parameters
        context: OOMOL context
        
    Returns:
        Dictionary containing video path and information
    """
    
    url = params["url"]
    output_dir = params.get("output_dir")
    format_spec = params.get("format", "best")
    filename_template = params.get("filename_template")
    quality = params.get("quality", "best")
    audio_only = params.get("audio_only", False)
    subtitle_langs = params.get("subtitle_langs")
    proxy = params.get("proxy")
    hdr = params.get("hdr", False)
    high_fps = params.get("high_fps", False)
    codec_preference = params.get("codec_preference", "h264")
    bitrate_limit = params.get("bitrate_limit")
    cookies_file = params.get("cookies_file")
    
    # Ensure output directory exists
    ensure_output_dir(output_dir)
    
    # Set default filename template
    if not filename_template:
        filename_template = get_default_filename_template()
    
    # Configure yt-dlp options
    format_to_use = format_spec if format_spec != "best" else get_format_string(quality, audio_only, hdr, high_fps, codec_preference, bitrate_limit)
    ydl_opts = create_ydl_options(output_dir, filename_template, format_to_use, proxy, cookies_file)
    
    # Configure audio and subtitle options
    ydl_opts = configure_audio_options(ydl_opts, audio_only)
    ydl_opts = configure_subtitle_options(ydl_opts, subtitle_langs)
    
    # Create progress hook
    progress_hook = create_progress_hook(context)
    ydl_opts['progress_hooks'] = [progress_hook]
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Display cookie status
            if cookies_file:
                if os.path.isfile(cookies_file):
                    print(f'🍪 Using cookies from: {cookies_file}')
                else:
                    print(f'⚠️ Cookie file not found: {cookies_file}')
            
            # Get video information first
            print('🔍 Extracting video information...')
            info = ydl.extract_info(url, download=False)
            
            # Display video information
            display_video_info(info, context)
            
            # Try to get optimal format for HD content
            if format_spec == "best" and quality in ['4K', '2160p', '1440p', '1080p']:
                optimal_format = get_optimal_format_for_hd(info, quality, hdr, high_fps, codec_preference)
                if optimal_format:
                    ydl_opts['format'] = optimal_format
                    print(f'🎯 Using optimized format for {quality} quality')
            
            # Display download start information
            display_download_info(quality, hdr, high_fps, codec_preference, context)
            
            # Update ydl_opts with final format
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_final:
                ydl_final.download([url])
            
            # Get actual downloaded file path
            filename = ydl.prepare_filename(info)
            if audio_only:
                # If audio only, extension will become .mp3
                base_name = os.path.splitext(filename)[0]
                filename = base_name + '.mp3'
            
            # Find the actual downloaded file
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')
            filename = find_downloaded_file(filename, output_dir, title, audio_only, ext)
            
            # Prepare output information
            video_info = prepare_video_info(info)
            
            return {
                'video_path': filename,
                'info': video_info
            }
            
    except Exception as e:
        print(f'Download failed: {str(e)}')
        raise Exception(f"Video download failed: {str(e)}")