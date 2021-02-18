from django.db import models
from django.contrib.auth.models import AbstractUser

_ = lambda tx: tx

class User(AbstractUser):
    balance     = models.IntegerField(_('Баланс'), default = 100,
                    help_text=_('Баланс пользователя в монетах'))
