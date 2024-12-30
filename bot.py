import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
import asyncio

# Настройки OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Генерация парадокса
async def generate_paradox():
    prompt = "Сгенерируй философский парадокс на тему технологий и сознания."
    try:
        # Новый метод для работы с актуальными моделями
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты генератор философских парадоксов."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Ошибка при вызове OpenAI API: {e}")
        return "Не удалось сгенерировать парадокс."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш нооскоп. Напишите /paradox, чтобы получить философский парадокс дня.")

# Команда /paradox
async def paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Генерирую парадокс, пожалуйста, подождите...")
    asyncio.create_task(send_paradox(update, context))

# Асинхронная обработка парадокса
async def send_paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        paradox = await generate_paradox()
        await update.message.reply_text(f"Парадокс дня:\n\n{paradox}")
    except Exception as e:
        logging.error(f"Ошибка при генерации парадокса: {e}")
        await update.message.reply_text("Произошла ошибка при генерации парадокса.")

# Основная функция
def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paradox", paradox))

    port = int(os.environ.get("PORT", 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=os.getenv("TELEGRAM_BOT_TOKEN"),
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_BOT_TOKEN')}"
    )

if __name__ == "__main__":
    main()
