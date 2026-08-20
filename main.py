#!/usr/bin/env python3
"""
Telegram Video Downloader Bot
Entry point for the application
"""

import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler
from telegram.ext import Application

from config import Config
from handlers.commands import setup_command_handlers
from handlers.callbacks import setup_callback_handlers
from utils.helpers import validate_bot_token

def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Configure UTF-8 encoding for console output on Windows
    if sys.platform.startswith('win'):
        try:
            import codecs
            import io
            # Only wrap if not already wrapped
            if not isinstance(sys.stdout, io.TextIOWrapper):
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
            if not isinstance(sys.stderr, io.TextIOWrapper):
                sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
        except Exception:
            # If encoding setup fails, continue without it
            pass
    
    # Configure logging with error handling
    try:
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                RotatingFileHandler(
                    'logs/bot.log',
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
    except Exception as e:
        # Fallback to basic logging if UTF-8 setup fails
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                RotatingFileHandler(
                    'logs/bot.log',
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
        print(f"Warning: UTF-8 logging setup failed: {e}")
    
    # Reduce noise from external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('yt_dlp').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    return logger

async def error_handler(update, context):
    """Global error handler"""
    logger = logging.getLogger(__name__)
    
    try:
        # Log the error
        logger.error(f"Exception while handling update {update}: {context.error}")
        
        # Try to inform the user
        if update and update.effective_message:
            error_message = (
                "❌ <b>An unexpected error occurred.</b>\n\n"
                "Please try again later or contact support if the problem persists."
            )
            
            try:
                await update.effective_message.reply_text(
                    error_message,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Failed to send error message to user: {e}")
    
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

def check_dependencies():
    """Check if all required dependencies are available"""
    logger = logging.getLogger(__name__)
    
    try:
        import yt_dlp
        logger.info(f"yt-dlp version: {yt_dlp.version.__version__}")
    except ImportError:
        logger.error("yt-dlp not found. Please install it with: pip install yt-dlp")
        return False
    
    try:
        import telegram
        logger.info(f"python-telegram-bot version: {telegram.__version__}")
    except ImportError:
        logger.error("python-telegram-bot not found. Please install it with: pip install python-telegram-bot")
        return False
    
    try:
        import dotenv
        logger.info("python-dotenv available")
    except ImportError:
        logger.error("python-dotenv not found. Please install it with: pip install python-dotenv")
        return False
    
    # Check for FFmpeg (optional but recommended for audio)
    import shutil
    if shutil.which('ffmpeg'):
        logger.info("FFmpeg found - audio extraction will work properly")
    else:
        logger.warning("FFmpeg not found - audio extraction may not work properly")
        logger.warning("Please install FFmpeg for full functionality (e.g. sudo apt install ffmpeg)")
    
    return True

def print_startup_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🎬 Telegram Video Downloader Bot 🎬               ║
║                                                              ║
║  Features:                                                   ║
║  • Download videos from YouTube, TikTok, Instagram & more    ║
║  • Extract audio in MP3, M4A, OGG formats                   ║
║  • Quality selection (720p, 1080p, Best)                    ║
║  • Progress tracking and rate limiting                       ║
║  • Support for 1000+ platforms via yt-dlp                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main function to start the bot"""
    
    # Setup logging
    logger = setup_logging()
    
    try:
        # Validate bot token
        if not validate_bot_token(Config.TELEGRAM_BOT_TOKEN):
            logger.error("Invalid Telegram bot token format. Please check your .env file.")
            sys.exit(1)
        
        logger.info("Starting Telegram Video Downloader Bot...")
        logger.info(f"Max file size: {Config.MAX_FILE_SIZE_MB}MB")
        logger.info(f"Download timeout: {Config.DOWNLOAD_TIMEOUT}s")
        logger.info(f"Rate limit: {Config.MAX_DOWNLOADS_PER_HOUR} downloads/hour")
        logger.info(f"Temp directory: {Config.TEMP_DIR}")
        
        # Create application
        application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Setup handlers
        setup_command_handlers(application)
        setup_callback_handlers(application)
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        logger.info("Bot handlers configured successfully")
        logger.info("Bot is starting... Press Ctrl+C to stop")
        
        # Run polling using PTB's built-in lifecycle management
        application.run_polling(
            allowed_updates=['message', 'callback_query'],
            drop_pending_updates=True
        )
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Print startup banner
    print_startup_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies. Please install required packages.")
        sys.exit(1)
    
    # Run the bot
    main()