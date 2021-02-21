from django.db import models
from django.core import mail
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .tokens import account_activation_token

_ = lambda tx: tx

class User(AbstractUser):
    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def send_confirmation_email(self, request = None):
        user = self
        current_site = get_current_site(request) if request else Site.objects.get(pk=settings.SITE_ID)
        mail_subject = f'{current_site.domain}: Активация аккаунта'
        message = render_to_string('emails/email_confirmation.html', {
            'user': self,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = self.email
        email = mail.send_mail(
                    mail_subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [to_email], html_message=message
        )
        # email.send()

    balance     = models.IntegerField(_('Баланс'), default = 100,
                    help_text=_('Баланс пользователя в монетах'))
    buyed_documents = models.ManyToManyField('main.Document', related_name='users_buyed', 
                    verbose_name=_('Купленный документы'), help_text=_('Список купленных пользователем документов'))
    email_confirmed = models.BooleanField(_('Email подтвержден'), default=True, null=False, blank=False)
