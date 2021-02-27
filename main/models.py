import datetime
import logging
import os.path
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import slugify as django_slugify
from django.shortcuts import reverse
from django.dispatch import receiver

from . import pages_count

BASE_PRICE = 10


_ = lambda tx: tx

FILE_TYPES = [
    ('pdf', 'PDF'),
    ('doc', 'Doc'),
    ('docx', 'Docx'),
    ('fb2', 'fb2'),
    ('djvu', 'Djvu'),
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

APPROVED_CHOICES = [
    (True, 'Принят'),
    (False, 'Отклонен'),
    (None, 'Не проверен'),
]

def year_choices():
    return [(r,r) for r in range(1990, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}
def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))



class Discipline(models.Model):
    class Meta:
        verbose_name         = _('Дисциплина')
        verbose_name_plural  = _('Дисциплины')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:discipline', args=[self.slug])

    @property
    def visible_documents(self):
        return self.documents.filter(approved=True)

    title = models.CharField(_('Название'), max_length=50)
    slug  = models.SlugField(_('Slug'), max_length=20, blank=True, null=True,
                    help_text=_("Это id который будет в URL страцы дисциплины. Должен быть на английском, без спецсимволов и пробелов."))
    # parent  = models.ForeignKey('Discipline', models.SET_NULL, null=True, blank=True, related_name='subdisciplines',
    #                 verbose_name=_('Главная дисциплина'), help_text="Дисциплина будет под-дисциплиной по отношению к выбранной")


class Document(models.Model):
    class Meta:
        verbose_name         = _('Документ')
        verbose_name_plural  = _('Документы')
        ordering             = ['-uploaded']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:document', args=[self.id])

    @property
    def file_download_url(self):
        return reverse("main:secure_document", args=[os.path.basename(self.file.name)])

    def get_file_size(self):
        if self.file_size:
            return f"{round(self.file_size, 2)} МБ."
        else:
            return "-"

    def save(self, *args, **kwargs):
        # Handle file
        if self.file:
            self.file_type = self.file.path.split(".")[-1] # Split ext and remove dot
            try:
                self.document_pages = pages_count.pages_count(self.file.path)
            except Exception as err:
                logging.exception("Pages counting error of document %s" % self.file.path, exc_info=err)
                self.document_pages = None
            try:
                self.file_size = os.path.getsize(self.file.path) / (1024 ** 2) # In MB
            except:
                self.file_size = None
            print(self.file_size)
        super().save(*args, **kwargs)

    title           = models.CharField(_('Заголовок'), max_length=50)
    type            = models.CharField(_('Тип работы'), choices=DOCUMENT_TYPES, max_length=20)
    created_year    = models.IntegerField(_('Год создания'), choices=year_choices(), default=current_year)
    annotation      = models.TextField(_('Аннотация'), blank=True, null=True)
    language        = models.CharField(_('Язык'), choices=settings.LANGUAGES, default=settings.LANGUAGES[0], max_length=5)
    discipline      = models.ForeignKey('Discipline', on_delete=models.SET_NULL, null=True, blank=True, related_name="documents",
                                    verbose_name=_('Дисциплина'))

    file            = models.FileField(upload_to='secure/documents', verbose_name=_('Файл'), null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=[ext for ext, tx in FILE_TYPES])])

    file_type       = models.CharField(_('Тип файла'), choices=FILE_TYPES,
                                     max_length=10, null=True, blank=True)

    file_size       = models.DecimalField(_('Размер файла'), null=True, blank=True, max_digits=5, decimal_places=2)

    document_pages  = models.IntegerField(_('Кол-во страниц'), null=True, blank=True)

    uploaded        = models.DateTimeField(_('Загружен'), editable=False, auto_now_add=True)
    approved        = models.BooleanField(_('Статус проверки'), default=True, null=True, blank=True, choices=APPROVED_CHOICES,
                                    help_text=_('Статус проверки загруженного документа модератором'))
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True, blank=True,
                                    verbose_name=_('Автор'))

#########################
###--- Plugins

# class TopMenu(models.Model):



##########################
###--- SIGNALS

@receiver(models.signals.pre_save, sender=Document)
def document_approving_state(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
        # print("Document created")
    else:
        if not obj.approved == instance.approved: # Field has changed
            old = obj.approved
            new = instance.approved
            author = obj.author
            #
            logging.info(f"Approving changed {old} => {new}")
            if new == True:# From any => approved
                author.balance += BASE_PRICE
                author.save()
                logging.info(f"Author balance is +{BASE_PRICE} !")
            elif old == True:# From approved => any
                author.balance += -BASE_PRICE
                author.save()
                logging.info(f"Author balance is -{BASE_PRICE} !")


@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Document` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).file
    except Document.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
