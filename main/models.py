import datetime
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


_ = lambda tx: tx

FILE_TYPES = [
    ('pdf', 'PDF'),
    ('word', 'Word'),
    ('fb2', 'fb2'),
]

DOCUMENT_TYPES = [
    ('essay', 'Реферат'),
    ('coursework', 'Курсовая работа'),
    ('thesis', 'Дипломная работа'),
    ('summary', 'Конспект'),
    ('lecture', 'Лекция'),
    ('test', 'Тест'),
    ('recomend', 'Методические рекомендации'),
]

def year_choices():
    return [(r,r) for r in range(1990, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year



class Discipline(models.Model):
    class Meta:
        verbose_name         = _('Дисциплина')
        verbose_name_plural  = _('Дисциплины')

    def __str__(self):
        return self.title

    title = models.CharField(_('Заголовок'), max_length=50)


class Document(models.Model):
    class Meta:
        verbose_name         = _('Документ')
        verbose_name_plural  = _('Документы')

    def __str__(self):
        return self.title

    title           = models.CharField(_('Заголовок'), max_length=50)
    type            = models.CharField(_('Тип работы'), choices=DOCUMENT_TYPES, max_length=20)
    created_year    = models.IntegerField(_('Год создания'), choices=year_choices(), default=current_year)
    annotation      = models.TextField(_('Аннотация'), blank=True, null=True)
    language        = models.CharField(_('Язык'), choices=settings.LANGUAGES, default=settings.LANGUAGES[0], max_length=5)
    discipline      = models.ForeignKey('Discipline', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name=_('Дисциплина'))

    file            = models.FileField(upload_to='documents', verbose_name=_('Файл'), null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=[ext for ext, tx in FILE_TYPES])])

    file_type       = models.CharField(_('Тип файла'), choices=FILE_TYPES,
                                     max_length=10, null=True, blank=True)

    document_pages  = models.IntegerField(_('Кол-во страниц'), null=True, blank=True)

    uploaded        = models.DateTimeField(_('Загружен'), editable=False, auto_now_add=True)
    approved        = models.BooleanField(_('Проверен'), default=None, null=True, blank=True,
                                    help_text=_('Статус проверки загруженного документа модератором'))
    author          = models.ForeignKey(User, models.CASCADE, null=True, blank=True,
                                    verbose_name=_('Автор'))
