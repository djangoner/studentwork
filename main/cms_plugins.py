from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from . import models

PAGE_ITEMS = _("Настриваемые элементы")

@plugin_pool.register_plugin
class TopMenuPlugin(CMSPluginBase):
    """
    Plugin for bootstrap 4 navbar
    @djangoner
    """
    # model = models.TopMenu
    module = PAGE_ITEMS
    # name of the plugin in the interface
    name = _("Верхнее меню")
    render_template = "plugins/top_menu.html"
    cache = False
    allow_children = True
    child_classes = ["LinkPlugin"]

    def render(self, context, instance, placeholder):
        #
        for child in instance.child_plugin_instances: # Patch links classes
            attrs = child.attributes
            if not 'class' in attrs:
                attrs['class'] = ''
            attrs['class'] += ' nav-link'
        #
        context = super().render(
            context, instance, placeholder)
        return context
