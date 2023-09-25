import random
from django.db import models
from datetime import timedelta, datetime, timezone
from configs import *
import json
import configs.models as config_models
from sorl.thumbnail import get_thumbnail


class Player(models.Model):
    userID = models.IntegerField(verbose_name="User Id", primary_key=True)
    carrots = models.IntegerField(default=0)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not Cooldown.objects.filter(user=self).exists():
            Cooldown.objects.create(user=self)

    def __str__(self) -> str:
        return str(self.userID)


class Rarity(models.Model):
    name = models.CharField(max_length=64)
    chance = models.PositiveIntegerField()
    emoji = models.CharField(max_length=64, blank=True, default="")

    @staticmethod
    def get_random():
        max_chance = 0
        rarities = Rarity.objects.all()
        for rarity in rarities:
            if Card.objects.filter(rarity=rarity).exists():
                max_chance += rarity.chance
        rand = random.randint(0, max_chance)
        for rarity in rarities:
            if Card.objects.filter(rarity=rarity).exists():
                if rand < rarity.chance:
                    return rarity
                else:
                    rand -= rarity.chance
        return Rarity.objects[0]

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.refresh_from_db()

    def __str__(self) -> str:
        return f"{self.name}-{self.chance}"


class Group(models.Model):
    name = models.CharField(verbose_name="GroupName", max_length=64)
    short = models.CharField(verbose_name="ShortName", default="", max_length=8)

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

    current_index = models.IntegerField(default=0, editable=False)

    image = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")

    @staticmethod
    def get_random():
        rarity = Rarity.get_random()
        return random.choice(Card.objects.filter(rarity=rarity))

    @staticmethod
    def get_random_from_group(group_name):
        rarity = Rarity.get_random()
        return random.choice(Card.objects.filter(rarity=rarity, group__name=group_name))

    def get_image(self, geometry) -> str:
        file = self.image.file if self.image else None
        return get_thumbnail(file, geometry, format="PNG").url

    def get_org_image(self) -> str:
        return  self.image.url if self.image else None

    def get_json(self, geometry) -> str:
        card_emoji = get_emoji("GENERIC_CARDS")
        arrow_emoji = get_emoji("GENERIC_RIGHTARROW")
        ls_emoji = get_emoji("GENERIC_LINESTART")

        card_desc = f"{card_emoji} **{self.get_id()}**:\n"
        card_desc += f"{arrow_emoji} **{self.group.name}**\n"
        card_desc += f"> {ls_emoji} **Era**: `{self.era.name}` \n"
        card_desc += f"> {ls_emoji} **Idol**: `{self.idol.name}` \n"
        card_desc += f"> {ls_emoji} **Type**: {self.rarity.emoji}"

        j = {
            "ID": self.cardUID,
            "CardDescription": card_desc,
            "url": self.get_image(geometry),
        }
        return json.dumps(j)

    def get_id(self):
        return self.cardUID + str(self.current_index + 1)

    def save(self, *args, **kwargs) -> None:
        self.cardUID = self.generate_id()
        super().save(*args, **kwargs)
        self.refresh_from_db()

    def generate_id(self) -> str:
        return f"{self.group.short}{self.era.short}{self.idol.short}K"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.cardUID}_{self.group.name}_{self.idol.name}_{self.era.name}"


class Inventory(models.Model):
    cardUID = models.CharField(unique=True, null=True, editable=False, max_length=64)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def get_info(self) -> str:
        card: Card = self.card
        return (f"{self.card.group.name}\n{self.card.era.name}\n>"
                f" {card.rarity.emoji} `{self.cardUID}` | `{self.card.idol.name}`")

    def get_view_json(self) -> str:
        card = self.card
        j = {
            "ID": card.cardUID,
            "card_id": card.cardUID,
            "owner": f"<@{self.user.userID}>",
            "type": card.rarity.emoji,
            "group": card.group.name,
            "era": card.era.name,
            "idol": card.idol.name,
            "url": card.get_org_image(),
        }
        return json.dumps(j)

    def __str__(self) -> str:
        return f"{self.user}({self.cardUID})"

    def generate_id(self):
        self.card.current_index += 1
        self.card.save()
        return self.card.cardUID + str(self.card.current_index)

    def save(self, *args, **kwargs) -> None:
        if not self.cardUID:
            self.cardUID = self.generate_id()
        super().save(*args, **kwargs)


class Cooldown(models.Model):
    user = models.OneToOneField(Player, primary_key=True, on_delete=models.CASCADE)
    lastDrop = models.DateTimeField(default=datetime.min)
    lastEpicDrop = models.DateTimeField(default=datetime.min)
    lastDaily = models.DateTimeField(default=datetime.min)
    lastWeekly = models.DateTimeField(default=datetime.min)
    lastClaim = models.DateTimeField(default=datetime.min)

    def gacha_remaining_time(self) -> timedelta:
        return self.get_remaining("DROP", self.lastDrop)

    def lucky_remaining_time(self) -> timedelta:
        return self.get_remaining("LUCKY", self.lastEpicDrop)

    def daily_remaining_time(self) -> timedelta:
        return self.get_remaining("DAILY", self.lastDaily)

    def weekly_remaining_time(self) -> timedelta:
        return self.get_remaining("WEEKLY", self.lastWeekly)

    def claim_remaining_time(self) -> timedelta:
        return self.get_remaining("CLAIM", self.lastClaim)

    def get_all_cooldowns(self) -> str:
        result = {
            "Drop": str(self.gacha_remaining_time()),
            "Lucky": str(self.lucky_remaining_time()),
            "Daily": str(self.daily_remaining_time()),
            "Weekly": str(self.weekly_remaining_time()),
            "Claim": str(self.claim_remaining_time()),
        }
        return json.dumps(result)

    def get_remaining(self, name, last_drop):
        cd, exist = config_models.Cooldown.objects.get_or_create(name=name)
        return last_drop + cd.duration - datetime.now(timezone.utc)

    def __str__(self) -> str:
        return str(self.user)


def get_emoji(name) -> str:
    return config_models.Emoji.get(name)
