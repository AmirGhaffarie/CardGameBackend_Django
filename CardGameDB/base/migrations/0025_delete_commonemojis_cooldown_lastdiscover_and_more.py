# Generated by Django 4.2.5 on 2023-10-22 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_playereracount_delete_commonemojis'),
    ]

    operations = [
        migrations.AddField(
            model_name='cooldown',
            name='lastDiscover',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='cooldown',
            name='lastStargaze',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]
