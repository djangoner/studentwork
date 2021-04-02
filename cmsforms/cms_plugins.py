from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from . import models
import blog.models

@plugin_pool.register_plugin
class CMSForm(CMSPluginBase):
    """
    CMS Plugin for editable bootstrap 4 forms
    @djangoner
    """
    name = _("CMS Форма")
    render_template = "plugins/cms_form.html"
    cache = False
    allow_children = True
    child_classes = [
        'FormTextField', 'FormTextAreaField', 
        'FormNumberField', 'FormFileField',
        'FormEmailField',
    ]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context


class CMSFormField(CMSPluginBase):
    """
    CMS Form field base
    @djangoner
    """
    name = _("Поле")
    model          = models.BaseField
    render_template= "plugins/field.html"
    cache = False
    require_parent = True
    parent_classes = ['CMSForm']
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        return context



@plugin_pool.register_plugin
class FormTextField(CMSFormField):
    name = _("Текстовое поле")
    render_template = "plugins/field_text.html"

@plugin_pool.register_plugin
class FormEmailField(FormTextField):
    name = _("Email поле")
    render_template = "plugins/field_email.html"

@plugin_pool.register_plugin
class FormTextAreaField(CMSFormField):
    name = _("Текстовое многострочное поле")
    render_template = "plugins/field_textarea.html"

@plugin_pool.register_plugin
class FormNumberField(CMSFormField):
    name = _("Числовое поле")
    render_template = "plugins/field_number.html"

@plugin_pool.register_plugin
class FormFileField(CMSFormField):
    name = _("Файловое поле")
    render_template = "plugins/field_file.html"
