"""
Configuration settings for the Telegram Video Downloader Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Bot settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    # Download settings - Telegram bot limit is 50MB
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))  # 50MB for Telegram bots
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 600))    # Increased timeout for larger files
    TEMP_DIR = os.getenv('TEMP_DIR', './downloads')
    
    # Rate limiting
    MAX_DOWNLOADS_PER_HOUR = int(os.getenv('MAX_DOWNLOADS_PER_HOUR', 5))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Cookie file support for YouTube / cloud IP authentication (e.g. cookies.txt)
    COOKIE_FILE = os.getenv('COOKIE_FILE', 'cookies.txt')
    
    # Ensure temp directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # yt-dlp base options
    YT_DLP_OPTIONS = {
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'extractaudio': False,
        'embed_subs': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'mweb', 'tv', 'web'],
            }
        }
    }
    
    # Automatically attach cookies file if present
    if os.path.exists(COOKIE_FILE):
        YT_DLP_OPTIONS['cookiefile'] = COOKIE_FILE

# Enhanced download options with video and audio support
DOWNLOAD_OPTIONS = {
    'video': {
        '360p': {
            'format': 'worst[height<=360]/worst[height<=480]/worst',
            'emoji': '📱',
            'description': '360p (Smallest)',
            'type': 'video'
        },
        '480p': {
            'format': 'worst[height<=480]/worst[height<=360]/worst',
            'emoji': '🎬',
            'description': '480p (Small)',
            'type': 'video'
        },
        'audio': {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'emoji': '🎵',
            'description': 'Audio Only (Smallest)',
            'type': 'video'
        }
    },
    'audio': {
        'mp3': {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'emoji': '🎵',
            'description': 'MP3 (Universal)',
            'type': 'audio'
        },
        'm4a': {
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192',
            }],
            'emoji': '🎼',
            'description': 'M4A (High Quality)',
            'type': 'audio'
        },
        'ogg': {
            'format': 'bestaudio[ext=webm]/bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'vorbis',
                'preferredquality': '192',
            }],
            'emoji': '🎶',
            'description': 'OGG (Open Source)',
            'type': 'audio'
        }
    }
}

# Error messages
ERROR_MESSAGES = {
    'rate_limit': "⏰ Rate limit exceeded. You can download {max_requests} videos per hour.\n⏳ Try again in {reset_time} minutes.",
    'invalid_url': "❌ Invalid URL format. Please provide a valid video URL.",
    'unsupported': "❌ This platform is not supported or the video is unavailable.",
    'file_too_large': "❌ Video file is too large (>50MB). Try selecting a lower quality.",
    'network_error': "❌ Network error. Please check your connection and try again.",
    'download_failed': "❌ Download failed. The video might be private or deleted.",
    'timeout': "❌ Download timeout. The video might be too large or server is slow.",
    'ffmpeg_missing': "❌ FFmpeg not found. Audio extraction requires FFmpeg to be installed.",
    'audio_extraction_failed': "❌ Failed to extract audio. The video might not contain audio.",
    'unsupported_audio_format': "❌ Audio format not supported for this video.",
    'audio_too_large': "❌ Audio file is too large (>50MB). Try a different format.",
    'no_audio_stream': "❌ No audio stream found in this video."
}

# Platform-specific error messages
PLATFORM_ERROR_MESSAGES = {
    'youtube': "❌ YouTube video unavailable. It might be private, deleted, or region-restricted.",
    'tiktok': "❌ TikTok video unavailable. It might be private or deleted.",
    'instagram': "❌ Instagram content unavailable. Private accounts are not supported.",
    'twitter': "❌ Twitter video unavailable. It might be private or deleted.",
    'generic': "❌ Video unavailable. The content might be private, deleted, or unsupported."
}