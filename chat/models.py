from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

FROM_WHO = [
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('system', 'Система'),
]

class ChatMessage(models.Model):
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Сообщение #{self.pk}"

    chat            = models.ForeignKey('Chat', models.CASCADE, verbose_name="Чат", related_name="messages")
    author          = models.CharField('От кого', choices=FROM_WHO, max_length=10)
    text            = models.TextField('Текст сообщения')
    sended          = models.BooleanField('Отправлено', default=False, null=False)
    readed          = models.BooleanField('Прочитано', default=False, null=False)
    created         = models.DateTimeField('Создано', auto_now_add=True, null=True)


class Chat(models.Model):
    def __str__(self):
        return f"Чат с {self.user}"

    def get_last_message(self):
        last_msg = self.messages.first()
        if last_msg:
            return last_msg.text

    user            = models.ForeignKey(User, models.CASCADE, verbose_name="Пользователь")
    created_at      = models.DateTimeField('Создан', auto_now_add=True, null=True)
