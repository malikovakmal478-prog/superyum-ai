import os
import asyncio
import logging
import requests
from threading import Thread
from flask import Flask

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# CONFIG
# ==========================

BOT_TOKEN = os.getenv("8321842423:AAG104h9Hz5V5N-4DysVGmrj4O0LMoVba00", "yordamvhi")
OPENROUTER_API_KEY = os.getenv("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")

MODEL = "deepseek/deepseek-chat-v3-0324:free"

SYSTEM_PROMPT = """
Siz o'zbek tilidagi professional AI yordamchisiz.
Har doim aniq, tushunarli va foydali javob bering.
Javoblarni o'zbek tilida yozing.
"""

# ==========================
# FLASK
# ==========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ishlayapti ✅"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# ==========================
# LOG
# ==========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# ==========================
# MEMORY
# ==========================

memory = {}
