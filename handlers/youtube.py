import yt_dlp
import os

async def download_video(update, context, url):
    try:
        ydl_opts = {
            'outtmpl': 'youtube.%(ext)s',
            'format': 'mp4',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            cmd = ["bin/yt-dlp", "--cookies", "cookies.txt", "-f", "mp4", "-o", f"{filename}.mp4, url]

        await update.message.reply_video(video=open(video_path, 'rb'))
        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text(f"❌ YouTube Error: {str(e)}")
