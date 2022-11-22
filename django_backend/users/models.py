from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    telegram_id = models.BigIntegerField(null=True, unique=True, blank=True)
