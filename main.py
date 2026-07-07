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
# ==========================
# OPENROUTER
# ==========================

def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60,
        )

        answer = r.json()["choices"][0]["message"]["content"]
        return answer

    except Exception as e:
        print(e)
        return "❌ AI javob bera olmadi."
        # ==========================
# COMMANDS
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Men SuperYum AI botiman.\n"
        "Savolingizni yozing."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    javob = ask_ai(text)

    if len(javob) > 4000:
        for i in range(0, len(javob), 4000):
            await update.message.reply_text(javob[i:i+4000])
   else:
    await update.message.reply_text(javob)


def main():
    Thread(target=run_flask).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("✅ Bot ishga tushdi...")

    application.run_polling()


if __name__ == "__main__":
    main()
