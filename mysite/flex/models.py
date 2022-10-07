"""
Flexible page
"""

from django.db import models
from streams import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.core import blocks as wagtail_blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class FlexPage(Page):
    """
    Flexible page class
    """

    template = "flex/flex_page.html"

    parent_page_types = [
        "flex.FlexPage",
        "home.HomePage",
    ]
    subpage_types = [
        "flex.FlexPage",
        "contacts.ContactPage",
    ]

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("richtext_block", blocks.RichtextBlock()),
            ("simple_richtext_block", blocks.SimpleRichtextBlock()),
            ("card_block", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
            ("button_block", blocks.ButtonBlock()),
            ("char_block", wagtail_blocks.CharBlock(
                required=True,
                help_text="This is an example help text",
                min_length=10,
                max_length=50,
                template="flex/char_block.html"
            ))
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Flex page"
        verbose_name_plural = "Flex Pages"
