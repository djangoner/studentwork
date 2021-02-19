from django.db import models
from django.contrib.auth.models import AbstractUser

_ = lambda tx: tx

class User(AbstractUser):
    balance     = models.IntegerField(_('Баланс'), default = 100,
                    help_text=_('Баланс пользователя в монетах'))
    buyed_documents = models.ManyToManyField('main.Document', related_name='users_buyed', 
                    verbose_name=_('Купленный документы'), help_text=_('Список купленных пользователем документов'))
