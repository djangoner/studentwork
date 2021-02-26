import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from main.models import FILE_TYPES

User = get_user_model()

FROM_WHO = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('system', 'Система'),
]

def is_admin(user):
    return user.is_superuser

def filter_is_admin(qs, val=False):
    return qs.filter(is_superuser=val)

class ChatMessage(models.Model):
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Сообщение #{self.pk}"
    

    def delete(self,*args,**kwargs):
        if self.attachment and os.path.isfile(self.attachment.path):
            os.remove(self.attachment.path)

        super().delete(*args,**kwargs)

    chat            = models.ForeignKey('Chat', models.CASCADE, verbose_name="Чат", related_name="messages")
    author          = models.CharField('От кого', choices=FROM_WHO, max_length=10)
    text            = models.TextField('Текст сообщения')
    sended          = models.BooleanField('Отправлено', default=False, null=False)
    readed          = models.BooleanField('Прочитано', default=False, null=False)
    created         = models.DateTimeField('Создано', auto_now_add=True, null=True)
    attachment      = models.FileField(upload_to='files/chat', null=True, blank=True, 
                                    verbose_name="Файл",
                                    validators=[FileExtensionValidator(allowed_extensions=[ext for ext, tx in FILE_TYPES])])


class Chat(models.Model):
    class Meta:
        ordering = ['last_message_sended']

    def __str__(self):
        return f"Чат с {self.user}"

    def get_last_message(self):
        last_msg = self.messages.first()
        if last_msg:
            return last_msg

    def get_unread(self, is_admin=False):
        if is_admin:
            return self.messages.filter(~models.Q(author="admin"), readed=False)
        else:
            return self.messages.filter(~models.Q(author="user"), readed=False)

    def get_unread_count(self, is_admin=False):
        return self.get_unread(is_admin=is_admin).count()

    def mark_readed(self, is_admin=False):
        return self.get_unread(is_admin=is_admin).update(readed=True)

    user            = models.ForeignKey(User, models.CASCADE, verbose_name="Пользователь")
    created_at      = models.DateTimeField('Создан', auto_now_add=True, null=True)
    last_message_sended= models.DateTimeField('Последнее отправленное сообщение', null=True)
