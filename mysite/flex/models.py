"""
Flexible page
"""

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


class FlexPage(Page):
    """
    Flexible page class
    """
    
    template = "flex/flex_page.html"

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    # @todo add streamfields
    # content = Streamfield()

    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]

    class Meta:
        verbose_name = "Flex page"
        verbose_name_plural = "Flex Pages"
