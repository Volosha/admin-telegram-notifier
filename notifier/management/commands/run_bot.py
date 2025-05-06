from django.core.management.base import BaseCommand
from notifier.bot import start_bot


class Command(BaseCommand):
    help = 'Запуск Telegram бота для уведомлений о входе в админку'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Запуск Telegram бота...'))
        start_bot()
