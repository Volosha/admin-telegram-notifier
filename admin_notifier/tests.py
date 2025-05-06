import pytest
from django.utils import timezone
from unittest.mock import patch, MagicMock, call, ANY
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import TelegramSubscriber
from .bot import send_admin_login_notification
from .signals import notify_telegram_on_admin_login


@pytest.mark.django_db
def test_subscriber_creation():
    """Тест создания модели подписчика"""
    subscriber = TelegramSubscriber.objects.create(chat_id='987654321')
    assert subscriber.chat_id == '987654321'
    assert subscriber.created_at is not None
    assert subscriber.created_at <= timezone.now()


@pytest.mark.django_db
def test_subscriber_string_representation():
    """Тест строкового представления модели"""
    subscriber = TelegramSubscriber.objects.create(chat_id='123456')
    assert str(subscriber) == "Subscriber 123456"


@pytest.mark.django_db
def test_subscriber_uniqueness():
    """Тест уникальности chat_id"""
    TelegramSubscriber.objects.create(chat_id='111222')
    with pytest.raises(Exception):  # Ожидаем ошибку при создании дубликата
        TelegramSubscriber.objects.create(chat_id='111222')


@pytest.mark.django_db
@patch('admin_notifier.bot.bot')
def test_send_notification_to_subscribers(mock_bot):
    """Тест отправки уведомлений подписчикам"""
    # Создаем тестовых подписчиков
    TelegramSubscriber.objects.create(chat_id='111')
    TelegramSubscriber.objects.create(chat_id='222')

    # Установка поведения мока
    mock_bot.send_message = MagicMock()

    # Вызов функции отправки уведомлений
    send_admin_login_notification('testadmin', timezone.now())

    # Проверка вызовов
    assert mock_bot.send_message.call_count == 2


@pytest.mark.django_db
@patch('admin_notifier.bot.bot')
def test_send_notification_no_subscribers(mock_bot):
    """Тест поведения при отсутствии подписчиков"""
    # Удаляем всех подписчиков если они есть
    TelegramSubscriber.objects.all().delete()

    # Установка поведения мока
    mock_bot.send_message = MagicMock()

    # Вызов функции отправки уведомлений
    send_admin_login_notification('testadmin', timezone.now())

    # Проверка, что функция отправки не вызывалась
    mock_bot.send_message.assert_not_called()





