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
