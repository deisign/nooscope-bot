import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import openai

# Загрузить переменные из окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8443))

# Настройка OpenAI API
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на команду /start."""
    await update.message.reply_text("Привет! Я ваш нооскоп.")

async def generate_paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация парадокса через OpenAI."""
    try:
        prompt = "Создай философский парадокс, который заставит задуматься."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        paradox = response["choices"][0]["message"]["content"]
        await update.message.reply_text(f"Вот парадокс: {paradox}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации парадокса: {e}")

# Создание приложения Telegram
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Обработчики команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("paradox", generate_paradox))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_BOT_TOKEN,
        webhook_url=f"https://172.236.3.175/{TELEGRAM_BOT_TOKEN}"
    )
