from unittest.util import _MAX_LENGTH

from django.db import models
from django.shortcuts import render
from streams import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet


class BlogAuthor(models.Model):
    """
    Blog author for snippets or plain data to be associated with a blog post
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("image"),
        ], heading="Name and Image"),
        MultiFieldPanel([
            FieldPanel("website"),
        ], heading="Links")
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogListingPage(RoutablePageMixin, Page):
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
        context["a_special_link"] = self.reverse_subpage("latest_posts")
        return context

    @route(r"^latest/?$", name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)
    
    def get_sitemap_urls(self, request=None):
        # Uncomment to have no sitemap for this page and its subpages
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location": self.full_url + self.reverse_subpage("latest_posts"),
            "lastmod": (self.last_published_at or self.latest_revision_created_at),
            "priority": 0.9,
        })
        return sitemap


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
