from email.policy import default

from django.db import models
from modelcluster.fields import ParentalKey
from streams import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page


class HomePageCarouselImages(Orderable):
    """
    Between 1 and 5 images for the home page carousel.
    """
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    panels = [
        FieldPanel("image")
    ]


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
        related_name="+",
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            FieldPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading="Banner Options"),
        MultiFieldPanel([
            InlinePanel("carousel_images", min_num=1, max_num=5, heading="Carousel Images")
        ], heading="Carousel Images"),
        FieldPanel("content"),
    ]


    # Set verbose names (implicitly set already)
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
