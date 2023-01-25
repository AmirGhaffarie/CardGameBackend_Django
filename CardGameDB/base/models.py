from django.utils.crypto import get_random_string
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from datetime import timedelta, datetime, timezone
import json


class Player(models.Model):
    userID = models.IntegerField(verbose_name="User Id", primary_key=True)
    balance = models.IntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not Cooldowns.objects.filter(user=self).exists():
            Cooldowns.objects.create(user=self)

    def __str__(self) -> str:
        return str(self.userID)


class Rarity(models.Model):
    name = models.CharField(max_length=64)
    chance = models.PositiveIntegerField()
    emoji = models.CharField(max_length=64, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.name}-{self.chance}"


class Group(models.Model):
    name = models.CharField(verbose_name="GroupName", max_length=64)
    short = models.CharField(verbose_name="ShortName", default="", max_length=8)
    emoji = models.CharField(
        verbose_name="Emoji", blank=True, default="", max_length=64
    )

    def save(self, *args, **kwargs) -> None:
        self.short = self.short.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Idol(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name="IdolName", max_length=64)
    short = models.CharField(verbose_name="ShortName", default="", max_length=8)

    def save(self, *args, **kwargs) -> None:
        self.short = self.short.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Era(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name="EraName", max_length=64)
    short = models.CharField(verbose_name="ShortName", default="", max_length=8)

    def save(self, *args, **kwargs) -> None:
        self.short = self.short.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Card(models.Model):
    cardUID = models.CharField(unique=True, editable=False, max_length=64)
    group = models.ForeignKey(Group, default=None, on_delete=models.RESTRICT)
    idol = models.ForeignKey(Idol, default=None, on_delete=models.RESTRICT)
    era = models.ForeignKey(Era, default=None, on_delete=models.RESTRICT)
    rarity = models.ForeignKey(Rarity, default=None, on_delete=models.RESTRICT)
    levels: str = models.CharField(
        validators=[validate_comma_separated_integer_list],
        default="1,4,10,25,50,100,150,200",
        max_length=128,
    )

    image1 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image2 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image3 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image4 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image5 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image6 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image7 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image8 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")

    def getImage(self, level) -> str:
        return {
            1: self.image1.url if self.image1 else None,
            2: self.image2.url if self.image2 else None,
            3: self.image3.url if self.image3 else None,
            4: self.image4.url if self.image4 else None,
            5: self.image5.url if self.image5 else None,
            6: self.image6.url if self.image6 else None,
            7: self.image7.url if self.image7 else None,
            8: self.image8.url if self.image8 else None,
        }[level]

    def getcurrentlevel(self, count):
        levels = self.levels.split(",")
        ints = [int(i) for i in levels]
        lowers = [i for i in ints if i <= count]
        return len(lowers), ints[len(lowers)] if len(lowers) < len(ints) else "max"

    def getJson(self, level) -> str:
        j = {
            "ID": self.cardUID,
            "Idol": self.idol.name,
            "Group": self.group.name,
            "Era": self.era.name,
            "url": f"{self.getImage(level)}",
        }
        return json.dumps(j)

    def getJsonWithLevel(self, level) -> str:
        j = {
            "Level": str(level),
            "ID": self.cardUID,
            "Idol": self.idol.name,
            "Group": self.group.name,
            "Era": self.era.name,
            "url": f"{self.getImage(level)}",
        }
        return json.dumps(j)

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            id = self.generate_id()
            while Card.objects.filter(cardUID=id).exists():
                id = self.generate_id()
            self.cardUID = id
        return super().save(*args, **kwargs)

    def generate_id(self) -> str:
        charset = "0123456789"
        Rn = get_random_string(length=3, allowed_chars=charset)
        return f"{self.group.short}{self.era.short}{self.idol.short}T{Rn}"

    def __str__(self) -> str:
        return f"{self.cardUID}_{self.group.name}_{self.idol.name}_{self.era.name}"


class Inventory(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def getInfo(self) -> str:
        card: Card = self.card
        level, next = card.getcurrentlevel(self.count)
        part1 = f"__{card.cardUID}__ {self.card.group.emoji}"
        part2 = f"**{card.idol.name}**({self.card.group.name})"
        part3 = f"({self.card.era.name})--**Level{level}**-({self.count}/{next})"
        return part1 + part2 + part3

    def getCard(self, level) -> str:
        card: Card = self.card
        current, next = card.getcurrentlevel(self.count)
        if level > current:
            return "none"
        elif level == 0:
            return card.getJsonWithLevel(current)
        else:
            return card.getJsonWithLevel(level)

    def __str__(self) -> str:
        return f"{self.user}({self.getInfo()})"


class Cooldowns(models.Model):
    user = models.OneToOneField(Player, primary_key=True, on_delete=models.CASCADE)
    lastDrop = models.DateTimeField(default=datetime.min)
    lastEpicDrop = models.DateTimeField(default=datetime.min)
    lastDaily = models.DateTimeField(default=datetime.min)
    lastWeekly = models.DateTimeField(default=datetime.min)
    lastClaim = models.DateTimeField(default=datetime.min)

    def dropRemainingTime(self) -> timedelta:
        return self.lastDrop + timedelta(minutes=5) - datetime.now(timezone.utc)

    def epicdropRemainingTime(self) -> timedelta:
        return self.lastEpicDrop + timedelta(minutes=20) - datetime.now(timezone.utc)

    def dailyRemainingTime(self) -> timedelta:
        return self.lastDaily + timedelta(days=1) - datetime.now(timezone.utc)

    def weeklyRemainingTime(self) -> timedelta:
        return self.lastWeekly + timedelta(days=7) - datetime.now(timezone.utc)

    def claimRemainingTime(self) -> timedelta:
        return self.lastClaim + timedelta(minutes=5) - datetime.now(timezone.utc)

    def getAllCooldowns(self) -> str:
        result = {
            "Drop": str(self.dropRemainingTime()),
            "EpicDrop": str(self.epicdropRemainingTime()),
            "Daily": str(self.dailyRemainingTime()),
            "Weekly": str(self.weeklyRemainingTime()),
            "Claim": str(self.claimRemainingTime()),
        }
        return json.dumps(result)

    def __str__(self) -> str:
        return str(self.user)
