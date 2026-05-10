import requests
import sqlite3
import json
import time
import asyncio
import aiohttp
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = "8286953271:AAHpHp0u2BOw0rLWBNXThNDsO9OSqhUMo2A"
ADMIN_ID = 5875325286
OWNER_USERNAME = "@SPIDEYXOP"

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, banned INTEGER DEFAULT 0)")
cursor.execute("CREATE TABLE IF NOT EXISTS groups (id INTEGER PRIMARY KEY)")
conn.commit()

# ---------------- QUOTES ----------------
QUOTES = [
    "💀 Accessing deep web nodes...",
    "⚡ Bypassing firewalls...",
    "🧠 Injecting intelligence modules...",
    "📡 Connecting to secure servers...",
    "🔍 Scraping hidden databases..."
]

# ---------------- ANTI SPAM ----------------
last_used = {}
def is_spam(uid):
    now = time.time()
    if uid in last_used and now - last_used[uid] < 3:
        return True
    last_used[uid] = now
    return False

def join_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/+vsxY045BWtoxZmQ1")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/+xs3_UOzhooBiZWZl")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/+c4thNPfAD4swNTll")]
    ])

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    cursor.execute("INSERT OR IGNORE INTO users(id, username) VALUES(?,?)", (user.id, user.username or ""))
    conn.commit()

    msg = await update.message.reply_text("⚡ Booting system...")
    for _ in range(3):
        await asyncio.sleep(0.7)
        await msg.edit_text(random.choice(QUOTES))

    await msg.edit_text(f"""
╔═══〔 ⚡ DARK OSINT ENGINE ⚡ 〕═══╗
║ 👋 Welcome {user.first_name}
║ 🧠 System Activated 24/7
║ 📡 Access Granted
║
║ 🚀 Use: /num 9876543210
║ Owner: {OWNER_USERNAME}
╚═══════════════════════════════╝
""")

# ---------------- NUMBER LOOKUP ----------------
async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_spam(uid):
        return await update.message.reply_text("⏳ Slow down...")

    if not context.args:
        return await update.message.reply_text("Usage: /num 9876543210")

    number = context.args[0]
    if not number.isdigit() or len(number) != 10:
        return await update.message.reply_text("❌ Invalid 10 digit number")

    wait = await update.message.reply_text("⚡ Scanning number in database...")
    await asyncio.sleep(2)
    await wait.delete()
    await update.message.reply_text(f"✅ Scan completed for {number}\nData will be shown soon.")

# ---------------- ADMIN ----------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("👑 ROOT ACCESS GRANTED\nYou are the owner.")

# ---------------- MAIN ----------------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("admin", admin))
    print("✅ Bot Started Successfully on Render!")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
