# Generated by Django 4.2.5 on 2023-09-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0004_rename_cooldowns_cooldown_rename_commonemojis_emoji"),
    ]

    operations = [
        migrations.CreateModel(
            name="Embed",
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
                (
                    "name",
                    models.CharField(max_length=64, unique=True, verbose_name="Name"),
                ),
                (
                    "emoji",
                    models.TextField(blank=True, default="", verbose_name="Embed"),
                ),
            ],
        ),
    ]
