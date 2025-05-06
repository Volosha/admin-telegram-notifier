import telebot
import logging
from django.conf import settings
from .models import TelegramSubscriber

logger = logging.getLogger(__name__)

# Инициализация бота
try:
    TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    logger.info("Telegram bot initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Telegram bot: {e}")
    bot = None


def start(message):
    """Обработчик команды /start для подписки на уведомления"""
    if bot is None:
        return

    chat_id = message.chat.id

    try:
        # Создаем или получаем подписчика
        subscriber, created = TelegramSubscriber.objects.get_or_create(chat_id=str(chat_id))

        if created:
            bot.reply_to(message, "Вы успешно подписались на уведомления о входе в админку!")
            logger.info(f"New subscriber: {chat_id}")
        else:
            bot.reply_to(message, "Вы уже подписаны на уведомления о входе в админку!")
            logger.info(f"Existing subscriber: {chat_id}")
    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        bot.reply_to(message, "Произошла ошибка при подписке на уведомления. Пожалуйста, попробуйте позже.")


def stop(message):
    """Обработчик команды /stop для отписки от уведомлений"""
    if bot is None:
        return

    chat_id = message.chat.id

    try:
        # Удаляем подписчика, если он существует
        try:
            subscriber = TelegramSubscriber.objects.get(chat_id=str(chat_id))
            subscriber.delete()
            bot.reply_to(message, "Вы успешно отписались от уведомлений о входе в админку!")
            logger.info(f"Subscriber removed: {chat_id}")
        except TelegramSubscriber.DoesNotExist:
            bot.reply_to(message, "Вы не были подписаны на уведомления!")
            logger.info(f"Non-existent subscriber tried to unsubscribe: {chat_id}")
    except Exception as e:
        logger.error(f"Error in /stop command: {e}")
        bot.reply_to(message, "Произошла ошибка при отписке от уведомлений. Пожалуйста, попробуйте позже.")


def send_admin_login_notification(username, login_time):
    """
    Отправка уведомлений всем подписчикам о входе в админку

    Args:
        username (str): Имя пользователя, который вошел в админку
        login_time (datetime): Время входа в админку
    """
    if bot is None:
        logger.warning("Telegram bot is not initialized. Notification not sent.")
        return

    try:
        subscribers = TelegramSubscriber.objects.all()

        if not subscribers:
            logger.warning("No subscribers to notify about admin login")
            return

        login_time_str = login_time.strftime("%d.%m.%Y %H:%M:%S")
        message = f"🔐 Вход в админку:\n📅 Дата: {login_time_str}\n👤 Пользователь: {username}"

        success_count = 0
        error_count = 0

        for subscriber in subscribers:
            try:
                bot.send_message(subscriber.chat_id, message)
                success_count += 1
                logger.info(f"Notification sent to {subscriber.chat_id}")
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to send notification to {subscriber.chat_id}: {e}")

        logger.info(f"Notification stats: {success_count} sent, {error_count} failed")

    except Exception as e:
        logger.error(f"Error sending admin login notifications: {e}")


def start_bot():
    """Запуск бота для прослушивания сообщений"""
    if bot is None:
        logger.error("Telegram bot is not initialized. Cannot start.")
        return

    try:
        # Регистрация обработчиков
        bot.message_handler(commands=['start'])(start)
        bot.message_handler(commands=['stop'])(stop)

        logger.info("Starting Telegram bot")
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Error while running Telegram bot: {e}")
