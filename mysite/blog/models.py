from django.db import models
from streams import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class BlogListingPage(Page):
    """
    Lists all the blogs
    """
    templates = "blog/blog_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailsPage.objects.live().public()
        return context


class BlogDetailsPage(Page):
    """
    Blog detail page
    """
    templates = "blog/blog_detail_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )    

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("richtext_block", blocks.RichtextBlock()),
            ("simple_richtext_block", blocks.SimpleRichtextBlock()),
            ("card_block", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("blog_image"),
        FieldPanel("content"),
    ]
