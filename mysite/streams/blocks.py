"""
Streamfields live in here
"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """
    Title and text and nothing else
    """
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class RichtextBlock(blocks.RichTextBlock):
    """
    Richtext with all the features
    """

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Richtext Block"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """
    Richtext with limited features
    """

    def __init__(
        self,
        required=True,
        help_text=None,
        editor="default",
        features=None,
        max_length=None,
        validators=(),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link"
        ]

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple Richtext Block"


class CardBlock(blocks.StructBlock):
    """
    Cards with image, text, and button
    """

    title = blocks.CharBlock(required=True, help_text="Add your title")
    cards = blocks.ListBlock(blocks.StructBlock([
        ("image", ImageChooserBlock(required=True)),
        ("title", blocks.CharBlock(required=True, max_length=40)),
        ("text", blocks.TextBlock(required=True, max_length=200)),
        ("button_page", blocks.PageChooserBlock(required=False)),
        ("button_url", blocks.URLBlock(
            required=False,
            help_text="If the button page above is selected, that will be used first"
        ))
    ]))

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"


class CTABlock(blocks.StructBlock):
    """
    A simple call to action section
    """
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=40)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    """
    Additional logic for the URLs, alternative to extending the context in a block.
    """
    def url(self):
        button_page = self.get("button_page")
        button_url = self.get("button_url")
        return button_page or button_url

    # def latest_posts(self):
    #     return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """
    An external or internal URL
    """
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
    #     return context
