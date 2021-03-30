from django.db import models
from cms.models.pluginmodel import CMSPlugin

class BaseField(CMSPlugin):
    label            = models.CharField("Название", max_length=50)
    name             = models.SlugField("HTML ID")
    placeholder_text = models.CharField("Замещающий текст", max_length=50, null=True, blank=True)
    required         = models.BooleanField("Обязательное поле", default=True)

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
