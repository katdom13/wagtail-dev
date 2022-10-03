from email.policy import default

from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
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
    banner_subtitle = RichTextField(features=["bold", "italic"], null=True, default="Subtitle Text")
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_image"),
        PageChooserPanel("banner_cta")
    ]


    # Set verbose names (implicitly set already)
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
