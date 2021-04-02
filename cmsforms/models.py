from django.db import models
from cms.models.pluginmodel import CMSPlugin

class BaseField(CMSPlugin):
    label            = models.CharField("Название поля", max_length=50,
                        help_text="Будет показано перед полем")

    name             = models.SlugField("ID (name) поля",
                        help_text="Должен быть уникальным! например: email_field, work_theme, work_type")

    placeholder_text = models.CharField("Замещающий текст", max_length=50, null=True, blank=True, 
                        help_text="Будет показано в поле, если поле пустое")

    required         = models.BooleanField("Обязательное поле", default=True,
                        help_text="Обязательно ли это поле для заполнения")

    hint             = models.CharField("Подсказка", max_length=250, blank=True,
                        help_text="Мелкий серый текст после поля, как этот")

    class Meta:
        verbose_name        = "Базовое поле"
        verbose_name_plural = "Базовые поля"
    #     abstract = True

    def __str__(self):
        return self.label

# class CustomField(BaseField):
#     field_type          = models.CharField("Тип поля", max_length=20, default="text",
#                         help_text="<input type='[тип поля]'>, по умолчанию text")

#     field_tag           = models.CharField("Тег поля", max_length=50,
#                         help_text="<tag type=\"...\" >")
    
    


# class TextField(BaseField):
#     pass

# class TextAreaField(BaseField):
#     pass

# class NumberField(BaseField):
#     pass

# class FileField(BaseField):
#     pass
