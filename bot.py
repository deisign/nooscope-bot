import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import openai
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8080))  # Используем порт 8080 для теста

# Настройка OpenAI API
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на команду /start."""
    logger.info("Получена команда /start")
    await update.message.reply_text("Привет! Я ваш нооскоп.")

async def generate_paradox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация парадокса через OpenAI."""
    logger.info("Получена команда /paradox")
    try:
        prompt = "Создай философский парадокс, который заставит задуматься."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        paradox = response["choices"][0]["message"]["content"]
        await update.message.reply_text(f"Вот парадокс: {paradox}")
    except Exception as e:
        logger.error(f"Ошибка при генерации парадокса: {e}")
        await update.message.reply_text(f"Ошибка при генерации парадокса: {e}")

# Создание приложения Telegram
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Обработчики команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("paradox", generate_paradox))

if __name__ == "__main__":
    # Тестовый HTTP-сервер для проверки порта
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Test server is running")

    # Запуск тестового сервера на порту 8080
    server = HTTPServer(("0.0.0.0", PORT), TestHandler)
    logger.info(f"Тестовый сервер запущен на порту {PORT}")
    server.serve_forever()
