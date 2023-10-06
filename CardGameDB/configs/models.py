from django.db import models
from datetime import timedelta


class Embed(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    embed = models.TextField(
        verbose_name="Embed", blank=True, default=""
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    @staticmethod
    def get(name) -> str:
        return Embed.objects.filter(name=name).first().emoji

    def __str__(self) -> str:
        return f"{self.name} : {self.embed[:5]}..."


class Emoji(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    emoji = models.CharField(
        verbose_name="Emoji", blank=True, default="", max_length=64
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    @staticmethod
    def get(name) -> str:
        return Emoji.objects.filter(name=name).first().emoji

    def __str__(self) -> str:
        return f"{self.name} : {self.emoji}"


class Cooldown(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    duration = models.DurationField(verbose_name="Duration", default=timedelta(0))

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} : {self.duration}"


class DiscoverItem(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    chance = models.PositiveIntegerField(verbose_name="Chance")
    amount = models.PositiveIntegerField(verbose_name="Amount")
    description = models.TextField(verbose_name="Description")

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"
