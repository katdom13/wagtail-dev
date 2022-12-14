# Generated by Django 4.1.1 on 2022-10-04 05:44

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_blogauthororderable"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        help_text="A slug to identify posts in this category",
                        max_length=255,
                        verbose_name="slug",
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog Category",
                "verbose_name_plural": "Blog Categories",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="blogdetailspage",
            name="categories",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.blogcategory"
            ),
        ),
    ]
