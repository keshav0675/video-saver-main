"""
Message templates and formatting for the Telegram Video Downloader Bot
"""

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format"""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def format_filesize(bytes_size: int) -> str:
    """Format file size in bytes to human readable format"""
    if not bytes_size:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

class MessageTemplates:
    @staticmethod
    def welcome_message() -> str:
        return (
            "🎬 <b>Video Downloader Bot</b>\n\n"
            "I can download videos from TikTok, Instagram, Twitter/X, Reddit, Facebook, Pinterest, Vimeo, and 1000+ other platforms!\n\n"
            "🚀 <b>How to use:</b>\n"
            "• Just send me any video URL\n"
            "• Or use the buttons below\n\n"
            "✨ <b>No commands needed!</b> Simply paste a link and I'll handle the rest!"
        )
    
    @staticmethod
    def help_message() -> str:
        return (
            "🆘 <b>Help - Video Downloader Bot</b>\n\n"
            "🚀 <b>How to Download:</b>\n"
            "1. Send me any video URL\n"
            "2. Choose Video or Audio\n"
            "3. Select quality/format\n"
            "4. Wait for your download!\n\n"
            "🌐 <b>Supported Platforms (1000+):</b>\n"
            "• 🎵 TikTok\n"
            "• 📸 Instagram\n"
            "• 🐦 Twitter / X\n"
            "• 🤖 Reddit\n"
            "• 📘 Facebook\n"
            "• 📌 Pinterest\n"
            "• 🎬 Vimeo, Dailymotion\n"
            "• 🔊 SoundCloud, Bandcamp\n"
            "• 🎮 Twitch Clips\n"
            "• ...and hundreds more!\n\n"
            "🎬 <b>Video Quality Options:</b>\n"
            "• 📱 360p / 480p - Fast download, smaller file\n"
            "• 🎬 Best - Highest available quality (up to 50MB)\n\n"
            "🎵 <b>Audio Format Options:</b>\n"
            "• 🎵 MP3 - Universal compatibility\n"
            "• 🎼 M4A - High quality, smaller size\n"
            "• 🎶 OGG - Open source format\n\n"
            "⚠️ <b>Limitations:</b>\n"
            "• Maximum file size: 50MB (Telegram limit)\n"
            "• Rate limit: 5 downloads per hour\n"
            "• Private content not supported\n\n"
            "💡 <b>Tip:</b> Just paste any video link - no commands needed!"
        )
    
    @staticmethod
    def content_type_selection(video_info: dict) -> str:
        platform_emoji = {
            'tiktok': '🎵',
            'instagram': '📸',
            'twitter': '🐦',
            'facebook': '📘',
            'reddit': '🤖',
            'pinterest': '📌',
            'vimeo': '🎬',
            'soundcloud': '🔊',
        }.get(video_info['platform'].lower(), '🎬')
        
        return (
            f"🎯 <b>Choose download type for:</b>\n"
            f"{platform_emoji} <b>{video_info['platform']}</b> - {video_info['title'][:50]}...\n\n"
            f"👤 <b>Uploader:</b> {video_info['uploader']}\n"
            f"⏱️ <b>Duration:</b> {format_duration(video_info['duration'])}\n\n"
            "What would you like to download?"
        )
    
    @staticmethod
    def quality_selection(content_type: str, video_info: dict) -> str:
        platform_emoji = {
            'tiktok': '🎵',
            'instagram': '📸',
            'twitter': '🐦',
            'facebook': '📘',
            'reddit': '🤖',
            'pinterest': '📌',
            'vimeo': '🎬',
            'soundcloud': '🔊',
        }.get(video_info['platform'].lower(), '🎬')
        
        type_text = "🎬 Video Quality" if content_type == 'video' else "🎵 Audio Format"
        
        return (
            f"🎯 <b>Choose {type_text.lower()} for:</b>\n"
            f"{platform_emoji} <b>{video_info['platform']}</b> - {video_info['title'][:50]}...\n\n"
            f"👤 <b>Uploader:</b> {video_info['uploader']}\n"
            f"⏱️ <b>Duration:</b> {format_duration(video_info['duration'])}\n\n"
            f"Select your preferred {type_text.lower()}:"
        )
    
    @staticmethod
    def download_starting(content_type: str, quality: str) -> str:
        type_emoji = "🎬" if content_type == 'video' else "🎵"
        action = "Downloading" if content_type == 'video' else "Extracting audio"
        
        return f"{type_emoji} <b>{action}...</b>\n📊 Preparing download..."
    
    @staticmethod
    def download_progress(percent: float, speed: str = "N/A") -> str:
        # Create progress bar
        filled = int(percent / 10)
        bar = "█" * filled + "░" * (10 - filled)
        
        return (
            f"⬇️ <b>Downloading...</b>\n"
            f"📊 Progress: [{bar}] {percent:.1f}%\n"
            f"🚀 Speed: {speed}"
        )
    
    @staticmethod
    def upload_starting() -> str:
        return "📤 <b>Uploading to Telegram...</b>\nPlease wait..."
    
    @staticmethod
    def download_complete(filename: str, filesize: int, content_type: str) -> str:
        type_emoji = "🎬" if content_type == 'video' else "🎵"
        type_text = "Video" if content_type == 'video' else "Audio"
        
        return (
            f"✅ <b>{type_text} Download Complete!</b>\n\n"
            f"📁 <b>File:</b> {filename}\n"
            f"📊 <b>Size:</b> {format_filesize(filesize)}\n\n"
            f"{type_emoji} Enjoy your {type_text.lower()}!"
        )
    
    @staticmethod
    def processing_url() -> str:
        return "🔍 <b>Analyzing video...</b>\nPlease wait..."
    
    @staticmethod
    def rate_limit_message(reset_time: int) -> str:
        return (
            f"⏰ <b>Rate Limit Exceeded</b>\n\n"
            f"You've reached the maximum of 5 downloads per hour.\n"
            f"⏳ Try again in {reset_time} minutes."
        )
    
    @staticmethod
    def invalid_url_message() -> str:
        return (
            "❌ <b>Invalid URL</b>\n\n"
            "Please provide a valid video URL.\n\n"
            "📝 <b>Usage:</b> /download &lt;video_url&gt;\n"
            "💡 <b>Example:</b> /download https://www.tiktok.com/@user/video/..."
        )
    
    @staticmethod
    def no_url_found_message() -> str:
        return (
            "🤔 <b>No video URL found!</b>\n\n"
            "Please paste a valid video link.\n\n"
            "💡 <b>Examples:</b>\n"
            "• TikTok: https://tiktok.com/@user/video/...\n"
            "• Instagram: https://instagram.com/reel/...\n"
            "• Twitter / X: https://x.com/user/status/...\n"
            "• Reddit: https://reddit.com/r/.../comments/..."
        )
    
    @staticmethod
    def download_prompt_message() -> str:
        return (
            "📥 <b>Paste your video link below</b>\n\n"
            "✨ Just send me the URL - I'll handle the rest!"
        )
    
    @staticmethod
    def main_menu_message() -> str:
        return (
            "🏠 <b>Main Menu</b>\n\n"
            "What would you like to do?\n\n"
            "💡 <b>Tip:</b> You can also just send me any video URL directly!"
        )
    
    @staticmethod
    def waiting_for_link_message() -> str:
        return (
            "⏳ <b>Waiting for your link...</b>\n\n"
            "📝 Please paste any video URL and I'll process it for you!\n\n"
            "🌐 <b>Supported platforms:</b> TikTok, Instagram, Twitter/X, Reddit, Facebook, Pinterest, and 1000+ more!"
        )