# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, unique=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    auth_token = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.telegram_username}"