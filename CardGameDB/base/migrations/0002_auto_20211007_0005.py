# Generated by Django 3.2.7 on 2021-10-06 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animeseries',
            old_name='animeName',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='cooldowns',
            old_name='userID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='cardID',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='cardCount',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='userID',
            new_name='user',
        ),
    ]