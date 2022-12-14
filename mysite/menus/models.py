from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


class MenuItem(Orderable):
    """
    Individual Menu content
    """
    link_title = models.CharField(
        blank=True,
        null=True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank=True
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"
    
    @property
    def title(self):
        if self.link_title:
            return self.link_title
        elif self.link_page:
            return self.link_page.title
        else:
            return "Missing Title"
    
    def save(self, *args, **kwargs):
        # Create a template fragment key
        key = make_template_fragment_key(
            "navigation"
        )

        # Delete the key
        cache.delete(key)

        return super().save(*args, **kwargs)


@register_snippet
class Menu(ClusterableModel):
    """
    The main menu parent
    """
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title
