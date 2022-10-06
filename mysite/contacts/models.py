from django.db import models
from modelcluster.models import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.fields import RichTextField
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(WagtailCaptchaEmailForm):
    """
    A whole page of an email contact form
    """

    template = "contacts/contact_page.html"
    landing_page_template = "contacts/contact_page_landing.html"

    parent_page_types = [
        "flex.FlexPage",
        "home.HomePage",
    ]
    subpage_types = []

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = WagtailCaptchaEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("from_address", classname="col6"),
                FieldPanel("to_address", classname="col6")
            ]),
            FieldPanel("subject"),
        ], heading="Email settings")
    ]
