#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Telegram Bot - ឆាតដូចជាសមាជិកធម្មតា
បង្កើតដោយប្រើ python-telegram-bot + Anthropic Claude
"""

import os
import json
import logging
import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# CONFIGURATION  (កំណត់នៅទីនេះ ឬប្រើ .env)
# ─────────────────────────────────────────────
BOT_TOKEN        = os.getenv("BOT_TOKEN",        "8241979149:AAHgcPjvR5tmkGfQmzqqu-H0_Fd_svwgJDk")
ANTHROPIC_KEY    = os.getenv("ANTHROPIC_API_KEY", "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")
OWNER_ID         = int(os.getenv("OWNER_ID",      "0"))   # Telegram user ID របស់អ្នកបង្កើត
SETTINGS_FILE    = "settings.json"

# ─────────────────────────────────────────────
# DEFAULT SETTINGS
# ─────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "bot_name": "សុខា",
    "personality": (
        "ខ្ញុំជាមនុស្សខ្មែរវ័យក្មេង រួសរាយ រាក់ទាក់ ចូលចិត្តជួយអ្នកដទៃ "
        "និងនិយាយដោយស្នាមញញឹម។"
    ),
    "rules": [
        "១. សូមប្រើភាសាសុភាព គ្មានការជេរ ឬបង្អាប់គ្នា",
        "២. ហាមវាយប្រហារ ឬអំពើហឹង្សាគ្រប់ប្រភេទ",
        "៣. ហាមដាក់លេខទំនាក់ទំនងឯកជន ឬការផ្សព្វផ្សាយ",
        "៤. ហាម Spam ឬ Forward សារដដែលៗ",
        "៥. សូមគោរព Admin និងសមាជិក",
        "៦. ប្រធានបទការពិភាក្សាត្រូវស្របច្បាប់",
    ],
    "welcome_message": (
        "🎉 សូមស្វាគមន៍ {name} មកកាន់ group យើង!\n"
        "សូមមើល /rules ដើម្បីដឹងអំពីវិធានក្រុម 📋"
    ),
    "max_tokens": 350,
    "respond_in_group": True,   # True = ឆ្លើយគ្រប់សារ, False = ឆ្លើយតែ mention/reply
}

# ─────────────────────────────────────────────
# SETTINGS HELPERS
# ─────────────────────────────────────────────
def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # merge ដើម្បីបន្ថែម key ថ្មីប្រសិនបើ settings.json ចាស់
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# AI RESPONSE (Claude Haiku)
# ─────────────────────────────────────────────
ai_client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

def get_ai_response(user_message: str, settings: dict, user_name: str) -> str:
    system_prompt = (
        f"អ្នកឈ្មោះ {settings['bot_name']}។ {settings['personality']}\n\n"
        f"អ្នកកំពុងនិយាយជាមួយ {user_name} នៅក្នុង Telegram group។\n"
        "ច្បាប់:\n"
        "- សរសេរជាភាសាខ្មែរ ធម្មជាតិ ដូចជាមនុស្សធម្មតា\n"
        "- ឆ្លើយខ្លី ១–៣ ប្រយោគ លើកលែងតែសំណួរចង់ដឹងបន្ថែម\n"
        "- ប្រើ emoji ដែលស័ក្តិសម (មិនច្រើនពេក)\n"
        "- កុំបង្ហាញថាអ្នកជា AI ឬ Bot ឡើយ\n"
        "- ធ្វើឱ្យការសន្ទនារស់រានមានជីវិត និងកក់ក្ដៅ"
    )
    try:
        resp = ai_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=settings.get("max_tokens", 350),
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        logger.error(f"AI Error: {e}")
        return "សូមទោស ខ្ញុំមានបញ្ហាបន្តិច សូមព្យាយាមម្តងទៀត 😅"


# ═══════════════════════════════════════════════
#  COMMAND HANDLERS
# ═══════════════════════════════════════════════

# ──────── /start ────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    user = update.effective_user
    welcome = settings["welcome_message"].format(name=user.first_name)
    await update.message.reply_text(
        f"{welcome}\n\n"
        f"💬 វាយ /rules ដើម្បីមើលវិធាន\n"
        f"🤖 ហៅ @{context.bot.username} ដើម្បីកុំ"
    )


# ──────── /rules ────────
async def cmd_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    rules_text = "\n".join(settings["rules"])
    await update.message.reply_text(
        f"📋 *វិធានក្រុម*\n\n{rules_text}\n\n"
        "⚠️ ការរំលោភវិធានណាមួយអាចនាំឱ្យបណ្តេញចេញ។",
        parse_mode="Markdown",
    )


# ──────── /setting (owner only) ────────
async def cmd_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != OWNER_ID:
        await update.message.reply_text("❌ តែម្ចាស់ Bot ប៉ុណ្ណោះដែលអាចប្រើពាក្យបញ្ជានេះ។")
        return

    settings = load_settings()
    respond_label = "✅ ឆ្លើយគ្រប់សារ" if settings["respond_in_group"] else "❌ ឆ្លើយតែ Mention/Reply"

    keyboard = [
        [InlineKeyboardButton("📝 ឈ្មោះ Bot", callback_data="set_name"),
         InlineKeyboardButton("🎭 បុគ្គលិកលក្ខណៈ", callback_data="set_personality")],
        [InlineKeyboardButton("📋 វិធាន", callback_data="set_rules"),
         InlineKeyboardButton("👋 សារស្វាគមន៍", callback_data="set_welcome")],
        [InlineKeyboardButton(f"💬 ឆ្លើយ Group: {respond_label}", callback_data="toggle_respond")],
        [InlineKeyboardButton("📊 ស្ថានភាព Bot", callback_data="bot_status")],
        [InlineKeyboardButton("🔄 Reset Default", callback_data="reset_settings")],
    ]
    await update.message.reply_text(
        f"⚙️ *ការកំណត់ Bot*\n\n"
        f"🤖 ឈ្មោះ: *{settings['bot_name']}*\n"
        f"💬 ឆ្លើយ Group: *{respond_label}*\n\n"
        "ជ្រើសរើសអ្វីដែលចង់កែ:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ═══════════════════════════════════════════════
#  CALLBACK QUERY HANDLER
# ═══════════════════════════════════════════════
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != OWNER_ID:
        await query.edit_message_text("❌ អ្នកមិនមានសិទ្ធិប្រើ Setting ទេ។")
        return

    settings = load_settings()
    data = query.data

    if data == "set_name":
        context.user_data["awaiting"] = "name"
        await query.edit_message_text(
            "📝 វាយ *ឈ្មោះថ្មី* សម្រាប់ Bot:\n_(ឧ. សុខា, វិចិត្រ, ចន្ទ្រា)_",
            parse_mode="Markdown",
        )

    elif data == "set_personality":
        context.user_data["awaiting"] = "personality"
        await query.edit_message_text(
            f"🎭 បុគ្គលិកលក្ខណៈបច្ចុប្បន្ន:\n_{settings['personality']}_\n\n"
            "វាយ *បុគ្គលិកលក្ខណៈថ្មី*:",
            parse_mode="Markdown",
        )

    elif data == "set_rules":
        current = "\n".join(settings["rules"])
        context.user_data["awaiting"] = "rules"
        await query.edit_message_text(
            f"📋 វិធានបច្ចុប្បន្ន:\n{current}\n\n"
            "វាយ *វិធានថ្មី* (មួយបន្ទាត់ = មួយវិធាន):",
            parse_mode="Markdown",
        )

    elif data == "set_welcome":
        context.user_data["awaiting"] = "welcome"
        await query.edit_message_text(
            f"👋 សារស្វាគមន៍បច្ចុប្បន្ន:\n_{settings['welcome_message']}_\n\n"
            "វាយ *សារថ្មី* (ប្រើ `{name}` សម្រាប់ឈ្មោះសមាជិក):",
            parse_mode="Markdown",
        )

    elif data == "toggle_respond":
        settings["respond_in_group"] = not settings["respond_in_group"]
        save_settings(settings)
        status = "✅ ឆ្លើយគ្រប់សារ" if settings["respond_in_group"] else "❌ ឆ្លើយតែ Mention/Reply"
        await query.edit_message_text(
            f"✅ បានប្តូរ!\nឥឡូវ Bot: *{status}*",
            parse_mode="Markdown",
        )

    elif data == "bot_status":
        respond_label = "ឆ្លើយគ្រប់សារ" if settings["respond_in_group"] else "ឆ្លើយតែ Mention/Reply"
        await query.edit_message_text(
            f"📊 *ស្ថានភាព Bot*\n\n"
            f"🤖 ឈ្មោះ: {settings['bot_name']}\n"
            f"🎭 បុគ្គលិកលក្ខណៈ:\n_{settings['personality'][:80]}..._\n\n"
            f"📋 វិធាន: {len(settings['rules'])} ចំណុច\n"
            f"💬 ការឆ្លើយ: {respond_label}\n"
            f"⚡ ស្ថានភាព: 🟢 Online",
            parse_mode="Markdown",
        )

    elif data == "reset_settings":
        save_settings(DEFAULT_SETTINGS.copy())
        await query.edit_message_text(
            "🔄 *ការកំណត់ត្រូវបាន Reset ទៅ Default រួចហើយ!*",
            parse_mode="Markdown",
        )


# ═══════════════════════════════════════════════
#  MESSAGE HANDLER
# ═══════════════════════════════════════════════
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user    = update.effective_user
    text    = update.message.text
    chat    = update.effective_chat
    settings = load_settings()

    # ── Owner setting input ──
    if user.id == OWNER_ID and "awaiting" in context.user_data:
        awaiting = context.user_data.pop("awaiting")

        if awaiting == "name":
            settings["bot_name"] = text.strip()
            save_settings(settings)
            await update.message.reply_text(
                f"✅ ឈ្មោះ Bot ត្រូវបានប្តូរទៅ *{text.strip()}* ✨",
                parse_mode="Markdown",
            )

        elif awaiting == "personality":
            settings["personality"] = text.strip()
            save_settings(settings)
            await update.message.reply_text("✅ បុគ្គលិកលក្ខណៈ Bot ត្រូវបានកំណត់ថ្មី!")

        elif awaiting == "rules":
            new_rules = [line.strip() for line in text.split("\n") if line.strip()]
            settings["rules"] = new_rules
            save_settings(settings)
            await update.message.reply_text(
                f"✅ វិធានត្រូវបានកំណត់ថ្មី! ({len(new_rules)} ចំណុច)"
            )

        elif awaiting == "welcome":
            settings["welcome_message"] = text.strip()
            save_settings(settings)
            await update.message.reply_text("✅ សារស្វាគមន៍ថ្មីត្រូវបានរក្សាទុក!")
        return

    # ── Determine whether bot should respond ──
    bot_username    = (await context.bot.get_me()).username
    is_private      = chat.type == "private"
    is_mentioned    = f"@{bot_username}" in text
    is_reply_to_bot = (
        update.message.reply_to_message is not None
        and update.message.reply_to_message.from_user.id == context.bot.id
    )
    should_respond_all = settings.get("respond_in_group", False)

    if not (is_private or is_mentioned or is_reply_to_bot or should_respond_all):
        return

    # Clean message
    clean = text.replace(f"@{bot_username}", "").strip() or "សួស្តី"

    # Typing indicator
    await context.bot.send_chat_action(chat_id=chat.id, action="typing")

    # Get AI response
    response = get_ai_response(clean, settings, user.first_name)
    await update.message.reply_text(response)


# ═══════════════════════════════════════════════
#  NEW MEMBER WELCOME
# ═══════════════════════════════════════════════
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = load_settings()
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        welcome = settings["welcome_message"].format(name=member.first_name)
        await update.message.reply_text(welcome)


# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════
def main():
    if BOT_TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
        logger.error("❌ BOT_TOKEN មិនទាន់កំណត់! សូមមើល README.md")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("rules",   cmd_rules))
    app.add_handler(CommandHandler("setting", cmd_setting))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(on_callback))

    # Messages
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message
    ))

    # New member
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member
    ))

    logger.info("✅ Bot កំពុងដំណើរការ... (Ctrl+C ដើម្បីឈប់)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
