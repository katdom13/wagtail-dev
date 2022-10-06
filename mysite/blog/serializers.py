# from rest_framework import serializers

# from .models import BlogAuthor


# class BlogAuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogAuthor
#         fields = (
#             "name",
#             "website"
#         )
from rest_framework.fields import Field


class ImageSerializerField(Field):
    """
    A custom serializer used in Wagtail v2 API
    """

    def to_representation(self, value):
        """
        Return the image url, title, and dimension
        """
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }
