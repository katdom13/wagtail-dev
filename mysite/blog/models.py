from unicodedata import category
from unittest.util import _MAX_LENGTH

from django import forms
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from rest_framework.fields import Field
from streams import blocks
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.models import register_snippet

# from blog.serializers import ImageSerializerField


class BlogCategory(models.Model):
    """
    Category for a blog
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify posts in this category"
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

register_snippet(BlogCategory)


class BlogAuthorOrderable(Orderable):
    """
    This allows us to select one or more blog authors from Snippets
    """
    page = ParentalKey("blog.BlogDetailsPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    @property
    def author_name(self):
        return self.author.name
    
    @property
    def author_website(self):
        return self.author.website
    
    @property
    def author_image(self):
        return self.author.image

    panels = [
        FieldPanel("author")
    ]

    api_fields = [
        APIField("author_name"),
        APIField("author_website"),
        # APIField("author_image", serializer=ImageSerializerField())
        APIField("rendered_image", serializer=ImageRenditionField(
            "fill-200x250",
            source="author_image",
        ))
    ]


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


class BlogChildPageSerializer(Field):
    def to_representation(self, child_pages):
        posts = []

        for child in child_pages:
            posts.append({
                "id": child.id,
                "title": child.title,
                "slug": child.slug,
                "url": child.url,
            })

        return posts

        # Pythonic comprehensions
        # return [
        #     {
        #         'id': child.id,
        #         'title': child.title,
        #         'slug': child.slug,
        #         'url': child.url,
        #     } for child in child_pages
        # ]


class BlogListingPage(RoutablePageMixin, Page):
    """
    Lists all the blogs
    """
    templates = "blog/blog_listing_page.html"
    ajax_template = "blog/blog_listing_page_ajax.html"

    parent_page_types = [
        "home.HomePage"
    ]
    subpage_types = [
        "blog.ArticlePage",
        "blog.VideoPage",
    ]

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    api_fields = [
        APIField("children", serializer=BlogChildPageSerializer(source="get_child_pages")),
    ]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

        # You can also bypass the serializer
        # return self.get_children().public().live().values("id", "title", "slug")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["a_special_link"] = self.reverse_subpage("latest_posts")
        context["categories"] = BlogCategory.objects.all()

        # Get all posts
        all_posts = BlogDetailsPage.objects.live().public().order_by("-first_published_at")

        # Get the category query if it exists
        category = request.GET.get("category")

        # Filter posts by category slug if category exists
        if category:
            all_posts = all_posts.filter(categories__slug__in=[category])
        
        # Get the tag query if it exists
        tags = request.GET.get("tag")

        if tags:
            all_posts = all_posts.filter(tags__slug__in=[tags])

        # Paginate all posts by 2
        paginator = Paginator(all_posts, 2)

        # Try to get page query ("?page=x")
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the page query is not an int, show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the page query is out of range, return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts

        return context

    @route(r"^july-2019/$", name="july_2019")
    @route(r"^year/(\d+)/(\d+)/$", name="blogs_by_year")
    def blogs_by_year(self, request, year=None, month=None, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        # Implement your BlogDetailPage filter. Maybe something like this:
        if year is not None and month is not None:
            all_posts = BlogDetailsPage.objects.live().public().filter(
                first_published_at__year=year, first_published_at__month=month)
        else:
            # No year and no month were set, assume this is july-2019 only posts
               all_posts = BlogDetailsPage.objects.live().public().filter(
                first_published_at__year=2019, first_published_at__month=7)

        context["posts"] = all_posts

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/blog_listing_page.html", context)

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug, *args, **kwargs):
        """
        Find blog posts based on category
        """
        context = self.get_context(request, *args, **kwargs)
        all_posts = BlogDetailsPage.objects.live().public().order_by("-first_published_at")

        try:
            # Look for the blog category by its slug.
            category = BlogCategory.objects.get(slug=cat_slug)
            all_posts = all_posts.filter(categories__in=[category])
        except BlogCategory.DoesNotExist:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            # Redirect to self.url, return a 404.. that's up to you!
            category = None
        
        if category is None:
            # This is an additional check.
            # If the category is None, do something. Maybe default to a particular category.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass

        paginator = Paginator(all_posts, 2)

        # Try to get page query ("?page=x")
        page = request.GET.get("page")

        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the page query is not an int, show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the page query is out of range, return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts

        return render(request, "blog/blog_listing_page.html", context)

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


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogDetailsPage",
        related_name="tagged_items",
        on_delete=models.CASCADE
    )


class BlogDetailsPage(Page):
    """
    Blog detail page
    """
    templates = "blog/blog_detail_page.html"

    parent_page_types = [
        "blog.BlogListingPage"
    ]
    subpage_types = []

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

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

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

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
        FieldPanel("tags"),
        FieldPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ], heading="Categories"),
        FieldPanel("content"),
    ]

    api_fields = [
        APIField("blog_authors"),
        APIField("content"),
    ]

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        # Create a template fragment key
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )

        # Delete the key
        cache.delete(key)

        return super().save(clean, user, log_action, **kwargs)


# First subclassed page
class ArticlePage(BlogDetailsPage):
    """
    A page specifically for articles based on a blog page
    """
    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Best size for this image is 1400x400"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        FieldPanel("tags"),
        FieldPanel("blog_image"),
        FieldPanel("intro_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ], heading="Categories"),
        FieldPanel("content"),
    ]


# Second subclassed page
class VideoPage(BlogDetailsPage):
    """
    A page specifically for videos based on a blog page
    """
    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("tags"),
        FieldPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
        ], heading="Author(s)"),
        MultiFieldPanel([
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
        ], heading="Categories"),
        FieldPanel("youtube_video_id"),
        FieldPanel("content"),
    ]
