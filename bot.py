import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

from handlers import tiktok, youtube, instagram, twitter
from handlers.TikTok import your_function_name
from handlers.Instagram import your_function_name
from handlers.Twitter import your_function_name
from handlers.YouTube import your_function_name


BOT_TOKEN = os.environ["BOT_TOKEN"]
user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 TikTok", callback_data='tiktok')],
        [InlineKeyboardButton("🎥 YouTube", callback_data='youtube')],
        [InlineKeyboardButton("📸 Instagram", callback_data='instagram')],
        [InlineKeyboardButton("🐦 Twitter", callback_data='twitter')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a platform:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data
    user_context[query.from_user.id] = platform
    await query.message.reply_text(f"✅ Selected {platform.capitalize()}. Now send the video link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    platform = user_context.get(user_id)

    if not platform:
        await update.message.reply_text("❗ Please choose a platform first using /start.")
        return

    handler_map = {
        "tiktok": tiktok.download_video,
        "youtube": youtube.download_video,
        "instagram": instagram.download_video,
        "twitter": twitter.download_video,
    }

    handler = handler_map.get(platform)
    if handler:
        await handler(update, context, url)
    else:
        await update.message.reply_text("🚫 Unsupported platform.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
