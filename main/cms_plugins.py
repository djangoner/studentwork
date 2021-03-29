from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from . import models
import blog.models

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
    cache = True
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

@plugin_pool.register_plugin
class DisciplinesListPlugin(CMSPluginBase):
    """
    Plugin for disciplines list
    """
    module = PAGE_ITEMS
    name   = _('Список дисциплин')
    render_template = "plugins/disciplines_list.html"
    cache = False
    allow_children = False

    def render(self, context, instance, placeholder):
        slice_rows = 3
        disciplines   = models.Discipline.objects.all().order_by('title')
        rows = []
        ##-- Slice to rows
        for i in range(0, slice_rows):
            rows.append(disciplines[i::slice_rows]) # Append sliced

        context.update({
            'disciplines': disciplines,
            'discipline_rows':rows,
        })
        return context

@plugin_pool.register_plugin
class BlogPostsPlugin(CMSPluginBase):
    """
    Plugin for several last blog posts
    """
    module = PAGE_ITEMS
    name = _("Последние посты блога")
    render_template = "plugins/blog_posts.html"
    cache = True

    def render(self, context, instance, placeholder):
        context['blog_posts'] = blog.models.Post.get_available()[:3]
        return context
