import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .bot import send_admin_login_notification

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def notify_telegram_on_admin_login(sender, request, user, **kwargs):
    """
    Сигнал, который отправляет уведомление в Telegram при входе в админку

    Args:
        sender: Отправитель сигнала
        request: HTTP запрос
        user: Пользователь, который выполнил вход
        **kwargs: Дополнительные аргументы
    """
    # Проверка, что запрос не пустой
    if request is None:
        logger.warning("Login signal received with no request object")
        return

    # Проверка пути запроса
    path = getattr(request, 'path', '')
    if not path:
        logger.warning("Request has no path attribute")
        return

    # Проверяем, что пользователь входит в админку и это не выход
    if path.startswith('/admin/') and not path.endswith('/logout/'):
        logger.info(f"Admin login detected: {user.username} at {timezone.now()}")

        # Отправляем уведомление
        send_admin_login_notification(user.username, timezone.now())
