from django.apps import AppConfig


class AdminNotifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_notifier'

    def ready(self):
        import admin_notifier.signals
