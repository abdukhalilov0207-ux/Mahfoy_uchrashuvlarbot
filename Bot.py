import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

ADMIN_ID = int(os.environ["ADMIN_ID"])

# Adminning botga kelgan xabarlari:
# admin_message_id -> foydalanuvchi_id
message_users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 🤍\n"
        "Bu anonim yozishma boti.\n"
        "Xabaringizni yozing."
    )


async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user

    # Adminning o'z xabarlarini bu yerda qayta ishlamaymiz
    if user.id == ADMIN_ID:
        if update.message.reply_to_message:
            admin_msg_id = update.message.reply_to_message.message_id
            target_user_id = message_users.get(admin_msg_id)

            if target_user_id:
                await context.bot.copy_message(
                    chat_id=target_user_id,
                    from_chat_id=ADMIN_ID,
                    message_id=update.message.message_id
                )
                await update.message.reply_text("✅ Xabaringiz yuborildi.")
            else:
                await update.message.reply_text(
                    "❌ Bu xabarning egasi topilmadi."
                )
        else:
            await update.message.reply_text(
                "Javob yuborish uchun foydalanuvchi xabariga Reply qiling."
            )
        return

    # Foydalanuvchidan xabar kelganda admin'ga yuboramiz
    sent = await context.bot.copy_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

    message_users[sent.message_id] = user.id

    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text="👤 Yangi anonim xabar\n"
                 "⬆️ Yuqoridagi xabarga Reply qilib javob bering."
        )
    except Exception:
        pass


def main():
    token = os.environ["BOT_TOKEN"]

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, user_message))

    app.run_polling()


if __name__ == "__main__":
    main()
