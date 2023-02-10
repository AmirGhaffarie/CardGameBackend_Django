from django.db import models
from datetime import timedelta, datetime, timezone

class CommonEmojis(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    emoji = models.CharField(
        verbose_name="Emoji", blank=True, default="", max_length=64
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} : {self.emoji}"

class Cooldowns(models.Model):
    name = models.CharField(verbose_name="Name", unique=True, max_length=64)
    duration = models.DurationField(verbose_name="Duration", default=timedelta(0))

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} : {self.duration}"
