from email.policy import default

from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from streams import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    TabbedInterface,
)
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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
        FieldPanel("image"),
    ]

    api_fields = [
        APIField("image"),
    ]


class HomePage(RoutablePageMixin, Page):
    """
    Home page model
    """

    # Already set implicitly, just wanted to be explicit
    templates = "home/home_page.html"

    # There can only be one instance of a home page per site
    # max_count = 1

    parent_page_types = [
        "wagtailcore.Page"
    ]
    subpage_types = [
        "blog.BlogListingPage",
        "contacts.ContactPage",
        "flex.FlexPage",
    ]

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
            InlinePanel("carousel_images", min_num=1, max_num=5, heading="Carousel Images")
        ], heading="Carousel Images"),
        FieldPanel("content"),
    ]

    # This is how you'd normally hide promote and settings tabs
    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            FieldPanel("banner_image"),
            PageChooserPanel("banner_cta"),
        ], heading="Banner Options"),
    ]

    # Overwrite the existing tabs and add an tab
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(banner_panels, heading="Banner"),
        ObjectList(Page.promote_panels, heading="Promote"),
        ObjectList(Page.settings_panels, heading="Settings"),
    ])

    # Exposes fields for the headless API (details page only)
    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta"),
        APIField("carousel_images"),
        APIField("content"),
    ]

    # Set verbose names (implicitly set already)
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"


    # A routable page is a page that wagtail has not much control with
    # Kind of an almost static subpage
    @route(r"^subscribe/?$")
    def subscribe(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)


# This will change the "title" field 's verbose name to "Custom Name".
# But you'd still reference it in the template as `page.title`
HomePage._meta.get_field("title").verbose_name = "Custom Name"

# Here we are removing the help text. But to change it, simply change None to a string.
HomePage._meta.get_field("title").help_text = None

# Below is the new default title for a Home Page.
# This only appears when you create a new page.
HomePage._meta.get_field("title").default = "Default Home Page Title"

# Lastly, we're adding a default `slug` value to the page.
# This does not need to reflect the same (or similar) value that the `title` field has.
HomePage._meta.get_field("slug").default = "default-homepage-title"
