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

class Outputs(typing.TypedDict):
    video_path: str
    info: dict

# endregion

import os
import json
import yt_dlp
from oocana import Context
from pathlib import Path

def main(params: Inputs, context: Context) -> Outputs:
    """
    使用 yt-dlp 下载视频
    
    Args:
        params: 输入参数
        context: OOMOL 上下文
        
    Returns:
        包含视频路径和信息的字典
    """
    
    url = params["url"]
    output_dir = params.get("output_dir", "/oomol-driver/oomol-storage/downloads")
    format_spec = params.get("format", "best")
    filename_template = params.get("filename_template", "%(title)s.%(ext)s")
    quality = params.get("quality", "best")
    audio_only = params.get("audio_only", False)
    subtitle_langs = params.get("subtitle_langs")
    proxy = params.get("proxy")
    
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 设置默认文件名模板
    if not filename_template:
        filename_template = "%(title)s.%(ext)s"
    
    # 配置 yt-dlp 选项
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, filename_template),
        'format': format_spec if format_spec != "best" else get_format_string(quality, audio_only),
    }
    
    # 仅下载音频
    if audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    # 字幕下载
    if subtitle_langs:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = subtitle_langs.split(',')
        ydl_opts['writeautomaticsub'] = True
    
    # 代理设置
    if proxy:
        ydl_opts['proxy'] = proxy
    
    # 进度回调
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            context.preview({
                'type': 'text',
                'data': f'下载进度: {percent} 速度: {speed} 剩余时间: {eta}'
            })
        elif d['status'] == 'finished':
            context.preview({
                'type': 'text',
                'data': f'下载完成: {d["filename"]}'
            })
    
    ydl_opts['progress_hooks'] = [progress_hook]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 获取视频信息
            info = ydl.extract_info(url, download=False)
            
            # 开始下载
            ydl.download([url])
            
            # 获取实际下载的文件路径
            filename = ydl.prepare_filename(info)
            if audio_only:
                # 如果是音频，扩展名会变成 .mp3
                base_name = os.path.splitext(filename)[0]
                filename = base_name + '.mp3'
            
            # 确保文件存在
            if not os.path.exists(filename):
                # 尝试查找实际下载的文件
                title = info.get('title', 'video')
                ext = 'mp3' if audio_only else info.get('ext', 'mp4')
                filename = os.path.join(output_dir, f"{title}.{ext}")
                
                # 如果还是找不到，使用通配符搜索
                if not os.path.exists(filename):
                    import glob
                    pattern = os.path.join(output_dir, f"{title}*")
                    files = glob.glob(pattern)
                    if files:
                        filename = max(files, key=os.path.getctime)
            
            # 准备输出信息
            video_info = {
                'title': info.get('title', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', ''),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
                'webpage_url': info.get('webpage_url', ''),
                'thumbnail': info.get('thumbnail', ''),
            }
            
            return {
                'video_path': filename,
                'info': video_info
            }
            
    except Exception as e:
        context.preview({
            'type': 'text',
            'data': f'下载失败: {str(e)}'
        })
        raise Exception(f"视频下载失败: {str(e)}")

def get_format_string(quality: str, audio_only: bool) -> str:
    """根据质量要求返回对应的格式字符串"""
    if audio_only:
        return 'bestaudio/best'
    
    quality_map = {
        'best': 'best',
        '1080p': 'best[height<=1080]',
        '720p': 'best[height<=720]',
        '480p': 'best[height<=480]',
        '360p': 'best[height<=360]',
    }
    
    return quality_map.get(quality, 'best')