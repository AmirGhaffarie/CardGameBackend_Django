import random
from django.db import models
from datetime import timedelta, datetime, timezone
from CardGameTestDB.game_configs import *
import json
import configs.models as config_models
from sorl.thumbnail import get_thumbnail


class Player(models.Model):
    userID = models.IntegerField(verbose_name="User Id", primary_key=True)
    carrots = models.IntegerField(default=0)

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
    level = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_from_xp(xp):
        level = xp / XP_PER_LEVEL
        for rarity in Rarity.objects.order_by("-level"):
            if level >= rarity.level:
                return rarity
        return Rarity.objects[0]

    @staticmethod
    def get_random():
        maxchance = 0
        rarities = Rarity.objects.order_by("level")
        for rarity in rarities:
            maxchance += rarity.chance
        rand = random.randint(0, maxchance)
        for rarity in rarities:
            if rand < rarity.chance:
                return rarity
            else:
                rand -= rarity.chance
        return Rarity.objects[0]

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.refresh_from_db()

    def get_index(self):
        return list(Rarity.objects.order_by("level")).index(self) + 1

    @staticmethod
    def get_by_index(index):
        return list(Rarity.objects.order_by("level"))[index - 1]

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

    current_index = models.IntegerField(default=0, editable=False)

    image1 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image2 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")
    image3 = models.ImageField(blank=True, upload_to="cardImages/%Y-%m")

    @staticmethod
    def get_random():
        return random.choice(Card.objects.all())

    @staticmethod
    def get_random_from_group(group):
        return random.choice(Card.objects.filter(group__name=group))

    def get_image(self, level, geometry) -> str:
        file = {
            1: self.image1.file if self.image1 else None,
            2: self.image2.file if self.image2 else None,
            3: self.image3.file if self.image3 else None,
        }[level]
        return get_thumbnail(file, geometry, format="PNG").url

    def get_org_image(self, level) -> str:
        return {
            1: self.image1.url if self.image1 else None,
            2: self.image2.url if self.image2 else None,
            3: self.image3.url if self.image3 else None,
        }[level]

    def get_json(self, level, geometry) -> str:
        card_emoji = get_emoji("GENERIC_CARDS")
        arrow_emoji = get_emoji("GENERIC_RIGHTARROW")
        ls_emoji = get_emoji("GENERIC_LINESTART")

    
        cardDesc = f"{card_emoji} **{self.cardUID}**:\n"
        cardDesc += f"{arrow_emoji} **{self.group.name}**\n"
        cardDesc += f"> {ls_emoji} **Era**: `{self.era.name}` \n"
        cardDesc += f"> {ls_emoji} **Idol**: `{self.idol.name}` \n"
        cardDesc += f"> {ls_emoji} **Type**: {Rarity.get_by_index(level).emoji}"

        j = {
            "ID": self.cardUID,
            "CardDescription": cardDesc,
            "url": self.get_image(level, geometry),
            "rarity_id": level,
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
    xp = models.PositiveIntegerField(default=0)

    def get_info(self) -> str:
        card: Card = self.card
        rarity = Rarity.get_from_xp(self.xp)
        return  f"{self.card.group.name}\n{self.card.era.name}\n> {rarity.emoji} `{self.cardUID}` | `{self.card.idol.name}`" 

    def get_view_json(self) -> str:
        rarity = Rarity.get_from_xp(self.xp)
        level = rarity.get_index()
        c_emoji = get_emoji("GENERIC_CARDS")
        np_emoji = get_emoji("GENERIC_NOTE")
        ls_emoji = get_emoji("GENERIC_LINESTART")

        cardDesc = f"{np_emoji} **{self.cardUID}** \n"
        cardDesc += f"> {c_emoji} **CARD INFO**: \n"
        cardDesc += f"> {ls_emoji} **Owner**: <@{self.user.userID}> \n"
        cardDesc += f"> {ls_emoji} **Type**: {rarity.emoji}\n"
        
        card = self.card
        cardDesc += f"> {ls_emoji} **Group**: `{card.group.name}` \n"
        cardDesc += f"> {ls_emoji} **Era**: `{card.era.name}` \n"
        cardDesc += f"> {ls_emoji} **Idol**: `{card.idol.name}`"

        j = {
            "ID": card.cardUID,
            "CardDescription": cardDesc,
            "url": card.get_org_image(level),
            "rarity_id": level,
        }
        return json.dumps(j)

    def get_rarity(self):
        return Rarity.get_from_xp(self.xp)

    def get_level(self):
        rarity = self.get_rarity()
        return self.xp // XP_PER_LEVEL - rarity.level + 1

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


class Cooldowns(models.Model):
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
        cd, exist = config_models.Cooldowns.objects.get_or_create(name=name)
        return last_drop + cd.duration - datetime.now(timezone.utc)

    def __str__(self) -> str:
        return str(self.user)


def get_emoji(name) -> str:
    return config_models.CommonEmojis.get_emoji(name)
