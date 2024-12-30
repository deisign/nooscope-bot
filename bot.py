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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты генератор философских парадоксов."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

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
    # Создание приложения Telegram
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paradox", paradox))

    # Настройка Webhook
    port = int(os.environ.get("PORT", 8443))  # Порт из переменных окружения
    app.run_webhook(
        listen="0.0.0.0",  # Слушать на всех интерфейсах
        port=port,  # Порт, указанный в Render
        url_path=os.getenv("TELEGRAM_BOT_TOKEN"),  # Путь для Webhook
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{os.getenv('TELEGRAM_BOT_TOKEN')}"  # Полный URL для Telegram Webhook
    )

if __name__ == "__main__":
    main()
