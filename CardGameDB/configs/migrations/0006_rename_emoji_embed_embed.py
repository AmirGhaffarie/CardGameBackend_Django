# Generated by Django 4.2.5 on 2023-09-25 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("configs", "0005_embed"),
    ]

    operations = [
        migrations.RenameField(
            model_name="embed",
            old_name="emoji",
            new_name="embed",
        ),
    ]