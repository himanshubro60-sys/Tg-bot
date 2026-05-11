import requests
import sqlite3
import json
import time
import asyncio
import aiohttp
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)

# ---------------- CONFIG ----------------

BOT_TOKEN = os.getenv("BOT_TOKEN", "8286953271:AAHpHp0u2BOw0rLWBNXThNDsO9OSqhUMo2A")
ADMIN_ID = 5875325286
OWNER_USERNAME = "@SPIDEYXOP"

CHANNELS = [
    "https://t.me/+vsxY045BWtoxZmQ1",
    "https://t.me/+xs3_UOzhooBiZWZl",
    "https://t.me/+c4thNPfAD4swNTll"
]

# ---------------- DATABASE ----------------

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    banned INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY
)
""")

conn.commit()

# ---------------- QUOTES ----------------

QUOTES = [
    "💀 Accessing deep web nodes...",
    "⚡ Bypassing firewalls...",
    "🧠 Injecting intelligence modules...",
    "📡 Connecting to secure servers...",
    "🔍 Scraping hidden databases...",
    "🚀 Initializing OSINT engine...",
    "⚔️ Breaking encryption layers..."
]

# ---------------- ANTI SPAM ----------------

last_used = {}

def is_spam(uid):
    now = time.time()
    if uid in last_used and now - last_used[uid] < 3:
        return True
    last_used[uid] = now
    return False

# ---------------- MULTI API ----------------

async def fetch_all_data(number):
    urls = [
        f"https://api.vectorxo.online/lookup?key=vectorxo&mobile={number}",
        f"https://ayaanmods.site/number.php?key=annonymous&number={number}",
        f"https://hitackgrop-19xe.vercel.app/get_data?key=loolo&mobile={number}",
        f"https://toxic-num-info.vercel.app/?number={number}"
    ]

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_api(session, url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for res in responses:
            if isinstance(res, dict):
                data = res.get("data") or res.get("result") or res
                if isinstance(data, list):
                    results.extend(data)
                elif isinstance(data, dict):
                    results.append(data)
    return results


async def fetch_api(session, url):
    try:
        async with session.get(url, timeout=5) as resp:
            return await resp.json()
    except:
        return {}

# ---------------- CLEAN ----------------

def clean_results(results):
    final = []
    seen = set()
    for r in results:
        if not isinstance(r, dict):
            continue
        mobile = str(r.get("mobile", "")).strip()
        name = str(r.get("name", "")).strip().lower()
        father = str(r.get("father", "")).strip().lower()
        address = str(r.get("address", "")).strip().lower()
        key = (mobile, name, father, address)
        if key not in seen:
            seen.add(key)
            final.append(r)
    return final

# ---------------- JOIN & BUTTON ----------------

async def is_joined(user_id, context):
    return True

def join_btn():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNELS[0])],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNELS[1])],
        [InlineKeyboardButton("📢 Join Channel 3", url=CHANNELS[2])]
    ])

# ---------------- SAVE GROUP ----------------

async def save_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:
        cursor.execute("INSERT OR IGNORE INTO groups(id) VALUES(?)", (update.effective_chat.id,))
        conn.commit()

# ---------------- SEND MSG ----------------

async def send_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        return await update.message.reply_text("❌ Usage: /send your message")
    text = " ".join(context.args)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"""
📩 NEW MESSAGE FROM USER

👤 Name: {user.first_name}
🆔 ID: {user.id}
📛 Username: @{user.username or 'no_username'}

💬 Message:
{text}
"""
    )
    await update.message.reply_text("✅ Message sent to admin")

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
║ 🧠 System Activated
║ 📡 Access Granted
║
║ 🚀 Use: /num 9876543210
║ /tg userid
║ /send msg
║ 🔐 Status: ACTIVE
║ Owner: {OWNER_USERNAME}
╚═══════════════════════════════╝

{random.choice(QUOTES)}
""")

# ---------------- TG ----------------

async def tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_spam(uid):
        return await update.message.reply_text("⏳ Slow down...")

    if not context.args:
        return await update.message.reply_text("Usage: /tg user_id")

    user_id = context.args[0]
    wait = await update.message.reply_text("⚡ Fetching TG data...")

    urls = [
        f"https://techvishalboss.com/api/v1/lookup.php?key=TVB_FULL_52F4672E&service=tg_to_number&telegram={user_id}",
        f"https://ayaanmods.site/sms.php?key=annonymoussms&term={user_id}",
        f"https://tg-number-api.vercel.app/?userid={user_id}",
        f"https://tg-number-api-wbka.vercel.app/?userid={user_id}"
    ]

    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(
            *[fetch_api(session, url) for url in urls],
            return_exceptions=True
        )

    results = []
    for data in responses:
        if not isinstance(data, dict):
            continue
        if "Number" in data:
            results.append({
                "number": data.get("Number"),
                "country": data.get("Country"),
                "brand": OWNER_USERNAME
            })
        else:
            d = data.get("data") or data.get("result") or data
            if isinstance(d, list):
                for x in d:
                    if isinstance(x, dict):
                        results.append({
                            "number": x.get("mobile") or x.get("number"),
                            "name": x.get("name"),
                            "alt": x.get("alt"),
                            "circle": x.get("circle") or x.get("region"),
                            "brand": OWNER_USERNAME
                        })
            elif isinstance(d, dict):
                results.append({
                    "number": d.get("mobile") or d.get("number"),
                    "name": d.get("name"),
                    "alt": d.get("alt"),
                    "circle": d.get("circle") or d.get("region"),
                    "brand": OWNER_USERNAME
                })

    await wait.delete()

    if not results:
        return await update.message.reply_text("❌ No data found")

    unique = []
    seen = set()
    for r in results:
        num = str(r.get("number"))
        if num and num != "None" and num not in seen:
            seen.add(num)
            unique.append(r)

    formatted = {
        "Powered_by": OWNER_USERNAME,
        "total_results": len(unique),
        "results": unique
    }

    json_output = json.dumps(formatted, indent=2)
    if len(json_output) > 4000:
        for i in range(0, len(json_output), 4000):
            await update.message.reply_text(f"```json\n{json_output[i:i+4000]}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"```json\n{json_output}\n```", parse_mode="Markdown")

# ---------------- AADHAR ------------------

async def aadhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_spam(uid):
        return await update.message.reply_text("⏳ Slow down...")

    if not context.args:
        return await update.message.reply_text("Usage: /aadhar 123412341234")

    aadhar_no = context.args[0]
    if not aadhar_no.isdigit():
        return await update.message.reply_text("❌ Invalid Aadhar number")

    wait = await update.message.reply_text("⚡ Fetching Aadhar data...")

    try:
        url = f"https://techvishalboss.com/api/v1/lookup.php?key=TVB_FULL_52F4672E&service=aadhar_to_number&number={aadhar_no}"
        r = requests.get(url, timeout=5)
        data = r.json()
    except:
        await wait.delete()
        return await update.message.reply_text("❌ API Error")

    await wait.delete()

    if not isinstance(data, dict):
        return await update.message.reply_text("❌ No valid data found")

    records = [data[key] for key in data if str(key).isdigit() and isinstance(data[key], dict)]

    unique = []
    seen = set()
    for r in records:
        mobile = str(r.get("mobile"))
        if mobile and mobile not in seen:
            seen.add(mobile)
            unique.append(r)

    formatted = {
        "Powered_by": OWNER_USERNAME,
        "service": "aadhar_lookup",
        "total_results": len(unique),
        "results": unique
    }

    json_output = json.dumps(formatted, indent=2)
    if len(json_output) > 4000:
        for i in range(0, len(json_output), 4000):
            await update.message.reply_text(f"```json\n{json_output[i:i+4000]}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"```json\n{json_output}\n```", parse_mode="Markdown")

# ---------------- NUMBER ----------------

async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_spam(uid):
        return await update.message.reply_text("⏳ Slow down...")

    cursor.execute("SELECT banned FROM users WHERE id=?", (uid,))
    res = cursor.fetchone()
    if res and res[0] == 1:
        return await update.message.reply_text("🚫 You are banned")

    if not context.args:
        return await update.message.reply_text("Usage: /num 9876543210")

    number = context.args[0]
    if not number.isdigit() or len(number) != 10:
        return await update.message.reply_text("❌ Invalid number")

    wait = await update.message.reply_text("⚡ Scanning...")

    raw = await fetch_all_data(number)
    results = clean_results(raw)

    await wait.delete()

    if not results:
        return await update.message.reply_text(f"❌ dear {update.effective_user.first_name} {number} is not in our database")

    formatted = []
    for r in results:
        data = {
            "NAME": r.get("name", "").upper() if r.get("name") else None,
            "fname": r.get("father", "").upper() if r.get("father") else None,
            "ADDRESS": r.get("address", ""),
            "circle": r.get("circle") or r.get("region") or r.get("operator") or None,
            "MOBILE": r.get("mobile", number),
            "alt": r.get("alt") or r.get("alternate") or r.get("alt_mobile") or None,
            "aadhar": r.get("aadhar") or r.get("aadhaar") or r.get("uid") or None,
            "id": r.get("id"),
            "email": r.get("email")
        }
        formatted.append(data)

    json_output = json.dumps(formatted, indent=2)
    if len(json_output) > 4000:
        for i in range(0, len(json_output), 4000):
            await update.message.reply_text(f"```json\n{json_output[i:i+4000]}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"```json\n{json_output}\n```", parse_mode="Markdown")

# ---------------- ADMIN ----------------

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = await update.message.reply_text("🔐 Accessing root control...")
    for _ in range(3):
        await asyncio.sleep(0.6)
        await msg.edit_text(random.choice(QUOTES))
    await msg.edit_text(f"""
╔══════════════════════════════╗
║ 👑  ROOT ACCESS TERMINAL 👑 ║
╠══════════════════════════════╣
║ ⚡ Welcome Boss {update.effective_user.first_name}
║ 🧠 Full System Control Granted
║
║ ── 🔥 USER CONTROL ──
║ 🚫 /ban <id>
║ ✅ /unban <id>
║
║ ── 📊 DATABASE ──
║ 👥 /userlist
║ 📡 /grouplist
║
║ ── 📢 BROADCAST ──
║ 📤 /broadcast <msg>
║ 📣 /broadcastgroup <msg>
║
║ ── 🎯 DIRECT CONTROL ──
║ ✉️ /dm <id> <msg>
║ 🚪 /leave <group_id>
║
╚══════════════════════════════╝

⚡ STATUS: ROOT MODE ACTIVE
Owner: {OWNER_USERNAME}
""")

# ---------------- ADMIN COMMANDS ----------------

async def ban(update, context):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        return await update.message.reply_text("❌ Usage: /ban <id>")
    uid = int(context.args[0])
    cursor.execute("UPDATE users SET banned=1 WHERE id=?", (uid,))
    conn.commit()
    await update.message.reply_text(f"✅ User {uid} has been banned successfully.")

async def unban(update, context):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        return await update.message.reply_text("❌ Usage: /unban <id>")
    uid = int(context.args[0])
    cursor.execute("UPDATE users SET banned=0 WHERE id=?", (uid,))
    conn.commit()
    await update.message.reply_text(f"✅ User {uid} has been unbanned successfully.")

async def userlist(update, context):
    if update.effective_user.id != ADMIN_ID: return
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    if not users:
        return await update.message.reply_text("❌ No users found")
    msg = "👥 USER DATABASE\n\n"
    for i, u in enumerate(users, 1):
        uid, username = u
        try:
            user = await context.bot.get_chat(uid)
            name = user.first_name
        except:
            name = "Unknown"
        msg += f"{i}. {name} (@{username or 'no_username'}) - {uid}\n"
        if len(msg) > 3500:
            await update.message.reply_text(msg)
            msg = ""
    if msg:
        await update.message.reply_text(msg)

async def grouplist(update, context):
    if update.effective_user.id != ADMIN_ID: return
    cursor.execute("SELECT id FROM groups")
    groups = cursor.fetchall()
    if not groups:
        return await update.message.reply_text("❌ No groups found")
    msg = "📡 GROUP DATABASE\n\n"
    for i, g in enumerate(groups, 1):
        gid = g[0]
        try:
            chat = await context.bot.get_chat(gid)
            name = chat.title
        except:
            name = "Unknown Group"
        msg += f"{i}. {name} - {gid}\n"
        if len(msg) > 3500:
            await update.message.reply_text(msg)
            msg = ""
    if msg:
        await update.message.reply_text(msg)

async def broadcastgroup(update, context):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        return await update.message.reply_text("❌ Usage: /broadcastgroup message")
    text = " ".join(context.args)
    cursor.execute("SELECT id FROM groups")
    sent = 0
    failed = 0
    msg = await update.message.reply_text("📡 Broadcasting to groups...")
    for g in cursor.fetchall():
        try:
            await context.bot.send_message(g[0], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1
    await msg.edit_text(f"📢 GROUP BROADCAST REPORT\n\n✅ Sent: {sent}\n❌ Failed: {failed}")

async def broadcast(update, context):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        return await update.message.reply_text("❌ Usage: /broadcast message")
    text = " ".join(context.args)
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    sent = 0
    failed = 0
    msg = await update.message.reply_text("📡 Broadcasting to users...")
    for u in users:
        try:
            await context.bot.send_message(u[0], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1
    await msg.edit_text(f"""
📢 BROADCAST REPORT

✅ Sent: {sent}
❌ Failed: {failed}
👥 Total: {len(users)}
""")

async def leave(update, context):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        return await update.message.reply_text("❌ Usage: /leave <group_id>")
    group_id = int(context.args[0])
    try:
        await context.bot.leave_chat(group_id)
        await update.message.reply_text(f"✅ Left group {group_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to leave: {e}")

# ---------------- MAIN (FIXED) ----------------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("tg", tg))
    app.add_handler(CommandHandler("aadhar", aadhar))
    app.add_handler(CommandHandler("send", send_msg))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("userlist", userlist))
    app.add_handler(CommandHandler("grouplist", grouplist))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("broadcastgroup", broadcastgroup))
    app.add_handler(CommandHandler("leave", leave))

    app.add_handler(MessageHandler(filters.ChatType.GROUPS | filters.ChatType.SUPERGROUP, save_group))

    print("✅ Bot started successfully on Railway!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
