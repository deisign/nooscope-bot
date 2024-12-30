import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Настройки OpenAI API из переменных окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Генерация парадокса
async def generate_paradox():
    prompt = "Сгенерируй философский парадокс на тему технологий и сознания."
    try:
        # Метод для версии openai==0.28
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        logging.error(f"Ошибка при вызове OpenAI API: {e}")
        return "Не удалось сгенерировать парадокс."

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш нооскоп. Напишите /paradox, чтобы получить философский парадокс дня.")

# Команда /paradox
async def paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        paradox_text = await generate_paradox()
        await update.message.reply_text(f"Парадокс дня:\n\n{paradox_text}")
    except Exception as e:
        logging.error(f"Ошибка при генерации парадокса: {e}")
        await update.message.reply_text("Произошла ошибка при генерации парадокса. Попробуйте позже.")

# Основная функция
def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Добавляем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paradox", paradox))

    # Настройка Webhook
    port = int(os.environ.get("PORT", 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=os.getenv("TELEGRAM_BOT_TOKEN"),
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_BOT_TOKEN')}"
    )

if __name__ == "__main__":
    main()
