import logging
import os  # Новый импорт для работы с переменными окружения
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Настройки OpenAI API из переменной окружения
openai.api_key = os.getenv("OPENAI_API_KEY")

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Генерация парадокса
async def generate_paradox():
    prompt = "Сгенерируй философский парадокс на тему технологий и сознания."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш нооскоп. Напишите /paradox, чтобы получить философский парадокс дня.")

# Команда /paradox
async def paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    paradox_text = await generate_paradox()
    await update.message.reply_text(f"Парадокс дня:\n\n{paradox_text}")

# Основная функция
def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("paradox", paradox))

    application.run_polling()

if __name__ == "__main__":
    main()
