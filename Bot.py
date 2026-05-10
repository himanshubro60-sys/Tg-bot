import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8286953271:AAHpHp0u2BOw0rLWBNXThNDsO9OSqhUMo2A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is Live 24/7!\n\nUse /num 9876543210")

async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /num 9876543210")
        return
    await update.message.reply_text(f"🔍 Scanning {context.args[0]}...")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", num))
    print("✅ Bot Started on Railway!")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
