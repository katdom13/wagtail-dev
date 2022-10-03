from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.models import Page


class HomePage(Page):
    """
    Home page model
    """

    # Already set implicitly, just wanted to be explicit
    templates = "home/home_page.html"

    # There can only be one instance of a home page per site
    max_count = 1

    banner_title = models.CharField(max_length=100, blank=False, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("banner_title")
    ]


    # Set verbose names (implicitly set already)
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
