from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# টেলিগ্রাম বট টোকেন
TELEGRAM_BOT_TOKEN = '7487129279:AAHAoPlnzFDtPzuZ1A8LbRkLpX7QMKxGAsc'

# Unsplash API কী
UNSPLASH_ACCESS_KEY = 'W6g32l19sIvu73nsWknuoMQWrlmcm9ejP_1-LW9jLDE'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('হ্যালো! একটি ছবি জেনারেট করতে, /generate লিখে একটি কিওয়ার্ড পাঠান। উদাহরণ: /generate sunset')

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ব্যবহারকারীর কিওয়ার্ড গ্রহণ করা
    keyword = ' '.join(context.args)
    if not keyword:
        await update.message.reply_text('দয়া করে একটি কিওয়ার্ড দিন। উদাহরণ: /generate sunset')
        return
    
    # Unsplash API ব্যবহার করে ছবি জেনারেট করা
    url = f'https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_ACCESS_KEY}'
    response = requests.get(url)
    
    # ত্রুটি হ্যান্ডলিং
    if response.status_code != 200:
        await update.message.reply_text('দুঃখিত, ছবি জেনারেট করতে সমস্যা হচ্ছে। পরে আবার চেষ্টা করুন।')
        return
    
    data = response.json()
    if 'urls' not in data:
        await update.message.reply_text('কোনও ছবি পাওয়া যায়নি। দয়া করে অন্য কিওয়ার্ড দিয়ে চেষ্টা করুন।')
        return

    photo_url = data['urls']['regular']
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=photo_url)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('generate', generate))

    application.run_polling()

if __name__ == '__main__':
    main()
