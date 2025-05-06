from django.db import models


class TelegramSubscriber(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscriber {self.chat_id}"

    class Meta:
        verbose_name = "Telegram Subscriber"
        verbose_name_plural = "Telegram Subscribers"
