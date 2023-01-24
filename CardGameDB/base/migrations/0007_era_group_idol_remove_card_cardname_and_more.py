# Generated by Django 4.1 on 2023-01-21 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_auto_20211107_2201"),
    ]

    operations = [
        migrations.CreateModel(
            name="Era",
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
                ("name", models.CharField(max_length=64, verbose_name="EraName")),
            ],
        ),
        migrations.CreateModel(
            name="Group",
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
                ("name", models.CharField(max_length=64, verbose_name="GroupName")),
            ],
        ),
        migrations.CreateModel(
            name="Idol",
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
                ("name", models.CharField(max_length=64, verbose_name="IdolName")),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="base.group"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="card",
            name="cardName",
        ),
        migrations.RemoveField(
            model_name="card",
            name="series",
        ),
        migrations.AlterField(
            model_name="card",
            name="image1",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image2",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image3",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image4",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image5",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image6",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image7",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="image8",
            field=models.ImageField(blank=True, upload_to="cardImages/%Y-%m"),
        ),
        migrations.AlterField(
            model_name="card",
            name="rarity",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.RESTRICT,
                to="base.rarity",
            ),
        ),
        migrations.DeleteModel(
            name="AnimeSeries",
        ),
        migrations.AddField(
            model_name="era",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="base.group"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="era",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.RESTRICT, to="base.era"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="group",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.RESTRICT, to="base.group"
            ),
        ),
    ]
