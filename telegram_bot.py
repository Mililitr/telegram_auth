import os
import django
import sys
import logging
import asyncio
import nest_asyncio
from asgiref.sync import sync_to_async

# Setup Django environment BEFORE importing Django models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth.settings')
django.setup()

# Now we can import Django models
from django.db import transaction
from django.contrib.auth.models import User
from telegram.ext import Application, CommandHandler
from telegram import Update
from accounts.models import TelegramUser

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Apply nest_asyncio patch
nest_asyncio.apply()

@sync_to_async
def create_or_update_telegram_user(telegram_id, username, token):
    with transaction.atomic():
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={'username': username}
        )
        
        telegram_user, created = TelegramUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'user': user,
                'telegram_username': username,
                'auth_token': token
            }
        )
        
        if not created:
            telegram_user.auth_token = token
            telegram_user.save()
        
        return created

async def start(update: Update, context):
    try:
        token = context.args[0] if context.args else None
        if not token:
            await update.message.reply_text("Please use the link from the website")
            return

        telegram_id = str(update.effective_user.id)
        username = update.effective_user.username or f"user_{telegram_id}"

        await create_or_update_telegram_user(telegram_id, username, token)
        await update.message.reply_text("Successfully authenticated! You can return to the website.")
        
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

async def main():
    try:
        app = Application.builder().token("7522481641:AAEwrWcbFb8bCnFEBAJp4x6MqOfq_hXNAPY").build()
        app.add_handler(CommandHandler("start", start))
        
        logger.info("Starting bot...")
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")