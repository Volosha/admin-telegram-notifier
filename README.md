

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Volosha/admin-telegram-notifier.git

cd admin-telegram-notifier
```

### 2. Настройка бота Telegram

1. Создайте бота через [@BotFather](https://t.me/BotFather) в Telegram
2. Получите токен бота
3. Создайте файл `.env` в корне проекта и добавьте токен:

```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
```

### 3. Запуск с помощью Docker

```bash
docker-compose up -d
```

### 4. Запуск без Docker

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Примените миграции:

```bash
python manage.py migrate
```

3. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

4. Запустите Django сервер:

```bash
python manage.py runserver
```

5. Запустите Telegram бота в отдельном терминале:

```bash
python manage.py run_bot
```

## Использование

1. Откройте бота в Telegram и отправьте команду `/start` для подписки на уведомления
2. Войдите в админку Django по адресу `http://localhost:8000/admin/`
3. Все подписанные пользователи получат уведомление о входе

Для отписки от уведомлений отправьте боту команду `/stop`.

## Тестирование

```bash
python manage.py test
```

или с использованием pytest:

```bash
pytest
```
