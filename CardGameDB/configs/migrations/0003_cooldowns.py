# Generated by Django 4.1.1 on 2023-02-09 21:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0002_alter_commonemojis_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cooldowns",
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
                    "duration",
                    models.DurationField(
                        default=datetime.timedelta(0), verbose_name="Duration"
                    ),
                ),
            ],
        ),
    ]
