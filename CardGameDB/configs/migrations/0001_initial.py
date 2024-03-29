# Generated by Django 4.1.1 on 2023-01-26 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommonEmojis",
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
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "emoji",
                    models.CharField(
                        blank=True, default="", max_length=64, verbose_name="Emoji"
                    ),
                ),
            ],
        ),
    ]
