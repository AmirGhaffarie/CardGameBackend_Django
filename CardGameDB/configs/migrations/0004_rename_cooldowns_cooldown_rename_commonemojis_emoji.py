# Generated by Django 4.2.5 on 2023-09-13 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0003_cooldowns"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Cooldowns",
            new_name="Cooldown",
        ),
        migrations.RenameModel(
            old_name="CommonEmojis",
            new_name="Emoji",
        ),
    ]
