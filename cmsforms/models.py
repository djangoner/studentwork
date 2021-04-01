from django.db import models
from cms.models.pluginmodel import CMSPlugin

class BaseField(CMSPlugin):
    label            = models.CharField("Название поля", max_length=50,
                        help_text="Будет показано перед полем")

    name             = models.SlugField("HTML ID",
                        help_text="Должен быть уникальным! например: email_field, work_theme, work_type")

    placeholder_text = models.CharField("Замещающий текст", max_length=50, null=True, blank=True, 
                        help_text="Будет показано в поле, если поле пустое")

    required         = models.BooleanField("Обязательное поле", default=True,
                        help_text="Обязательно ли это поле для заполнения")

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

class TextField(BaseField):
    pass

class TextAreaField(BaseField):
    pass

class NumberField(BaseField):
    pass

class FileField(BaseField):
    pass
