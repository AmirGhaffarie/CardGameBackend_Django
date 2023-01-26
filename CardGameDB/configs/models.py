from django.db import models

# Create your models here.


class CommonEmojis(models.Model):
    name = models.CharField(verbose_name="Name", max_length=64)
    emoji = models.CharField(
        verbose_name="Emoji", blank=True, default="", max_length=64
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.emoji}_{self.name}"
