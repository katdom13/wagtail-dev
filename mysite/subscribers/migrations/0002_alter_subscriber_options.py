# Generated by Django 4.1.1 on 2022-10-03 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscribers", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscriber",
            options={"verbose_name": "Subscriber", "verbose_name_plural": "Subcribers"},
        ),
    ]
