import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAILWAY_URL = os.getenv("RAILWAY_URL")  # Например: https://telegramgptbot-production.up.railway.app

openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = """
Ты — эксперт по металлорежущему инструменту в компании ИНТЕР ПРОМ. Помогаешь отделу продаж подбирать фрезы, сверла, резцы и т.п. под материалы, режимы, станки. Отвечай профессионально, понятно и по делу.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    )
    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    PORT = int(os.environ.get("PORT", "8443"))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{RAILWAY_URL}/{BOT_TOKEN}"
    )
