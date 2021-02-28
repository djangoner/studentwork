from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify as django_slugify
from ckeditor.fields import RichTextField
from django.shortcuts import reverse
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

_ = lambda tx: tx

User = get_user_model()

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}
def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))




class Tag(models.Model):
    class Meta:
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog') + f"?tag={self.pk}"


    name        = models.CharField(_("Название"), max_length=50)
    slug        = models.SlugField(_("Префикс URL"), null=True, blank=True,
                        help_text="Если пустой, то генерируется автоматически.")


class Post(models.Model):
    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')
        ordering = ['is_publicated', '-publicated']

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.publicated:
            self.publicated = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_post', args=[self.pk])

    def get_annotation(self):
        length  = 450
        text    = strip_tags(self.content)
        if len(text) > length:
            text = text[:length] + "..."
        #
        return text


    title       = models.CharField(_("Заголовок"), max_length=100)
    content     = RichTextField(_("Содержание"), config_name='blog_post_content')

    tags        = models.ManyToManyField('Tag', verbose_name=_("Теги"))
    is_publicated= models.BooleanField(_("Опубликовано"), default=False)
    created     = models.DateTimeField(_("Создано"), auto_now_add=True)
    publicated  = models.DateTimeField(_("Опубликовано"), null=True, blank=True, 
                        help_text="Заполняется автоматически при публикации")



class PostComment(models.Model):
    class Meta:
        verbose_name = _('Комментарий к посту')
        verbose_name_plural = _('Комментарии к посту')

    def __str__(self):
        return f"{self.text}"

    post        = models.ForeignKey('Post', models.CASCADE, verbose_name=_('Пост'), related_name="comments")
    author      = models.ForeignKey(User, models.CASCADE, verbose_name=_('Автор поста'))
    text        = models.TextField(_('Содержимое'), max_length=500)
    created     = models.DateTimeField(_('Создан'), auto_now_add=True, editable=False)
