from datetime import timedelta, datetime, timezone
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import GroupName, Card, Cooldowns, Inventory, Player, Rarity
import random
from .paginations import InventoryPaginaiton
from .serializers import InventorySerializer
from rest_framework.generics import ListAPIView


def register(request, id):
    if Player.objects.filter(userID=id).exists():
        return HttpResponse(content="Account already exists.")
    else:
        player = Player(userID=id)
        player.save()
        return HttpResponse(content="Account registered successfully.")


def cds(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    return HttpResponse(cd.getAllCooldowns())


def balance(request, id):
    player = get_object_or_404(Player, userID=id)
    return HttpResponse(player.balance)


def claim(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    cd.lastClaim = datetime.now(timezone.utc)
    cd.save()
    return HttpResponse(content="Success")


def drop(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    if cd.dropRemainingTime() > timedelta(0):
        return HttpResponse(status=210, content=str(cd.dropRemainingTime()))
    else:
        cd.lastDrop = datetime.now(timezone.utc)
        cd.save()
        item = getRandomCard()
        return HttpResponse(item.getJson(1))


def daily(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    if cd.dailyRemainingTime() > timedelta(0):
        return HttpResponse(status=210, content=str(cd.dailyRemainingTime()))
    else:
        cd.lastDaily = datetime.now(timezone.utc)
        cd.save()
        item = getRandomCard2()
        return HttpResponse(item.getJson(1))


def weekly(request, id, anime):
    cd = get_object_or_404(Cooldowns, user=id)
    if cd.weeklyRemainingTime() > timedelta(0):
        return HttpResponse(status=210, content=str(cd.weeklyRemainingTime()))
    elif GroupName.objects.filter(name=anime).exists():
        cd.lastWeekly = datetime.now(timezone.utc)
        cd.save()
        recs = []
        dic = {}
        recs.append(getRandomAnimeCard(anime).getJson(1))
        recs.append(getRandomAnimeCard(anime).getJson(1))
        dic["res"] = recs
        return JsonResponse(dic)
    else:
        return HttpResponse(status=220, content="Group you entered not Exists")


def epicdrop(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    if cd.epicdropRemainingTime() > timedelta(0):
        return HttpResponse(status=210, content=str(cd.epicdropRemainingTime()))
    else:
        cd.lastEpicDrop = datetime.now(timezone.utc)
        cd.save()
        recs = []
        dic = {}
        recs.append(getRandomCard().getJson(1))
        recs.append(getRandomCard().getJson(1))
        recs.append(getRandomCard().getJson(1))
        dic["res"] = recs
        return JsonResponse(dic)


def gift_card(request, id_from, id_to, cardid, amount):
    user_from = get_object_or_404(Player, userID=id_from)
    user_to = get_object_or_404(Player, userID=id_to)
    card = get_object_or_404(Card, cardUID=cardid)
    inv_from = Inventory.objects.get_or_create(user=user_from, card=card)[0]
    inv_to = Inventory.objects.get_or_create(user=user_to, card=card)[0]
    if inv_from.count >= amount:
        inv_from.count -= amount
        inv_to.count += amount
        inv_from.save()
        inv_to.save()
        return HttpResponse("Success")
    else:
        return HttpResponse(status=210, content="Not enough cards")


def check_having_cards(request, id, cardid, amount):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=cardid)
    inv = Inventory.objects.get_or_create(user=user, card=card)[0]
    if inv.count >= amount:
        return HttpResponse("Success")
    else:
        return HttpResponse(status=210, content="Not enough cards")


def addcard(request, id, cardid, amount):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=cardid)
    inv = Inventory.objects.get_or_create(user=user, card=card)[0]
    if (inv.count + amount) >= 0:
        inv.count += amount
        inv.save()
        return HttpResponse(content="Success")
    else:
        return HttpResponse(status=210, content="Not enough cards")


def change_balance(request, id, amount):
    user = get_object_or_404(Player, userID=id)
    if (user.balance + amount) >= 0:
        user.balance += amount
        user.save()
        return HttpResponse(content="Success")
    else:
        return HttpResponse(status=210, content="Not enough money")


def viewcard(request, userid, cardid, level):
    user = get_object_or_404(Player, userID=userid)
    inv = get_object_or_404(Inventory, user=user, card__cardUID=cardid)
    card = inv.getCard(level)
    if card == "none":
        return HttpResponse(
            status=210, content="The player does not have that level of the card"
        )
    else:
        return HttpResponse(content=card)


class InventoryView(ListAPIView):
    def get(self, request, id, format=None):
        res = Inventory.objects.filter(user=id).exclude(count=0).order_by("count")
        paginator = InventoryPaginaiton()
        pag = paginator.paginate_queryset(res, request)
        invs = InventorySerializer(pag, many=True)
        pag = paginator.get_paginated_response(invs.data)
        return pag


# utilities
def getRandomCard():
    rar = getRandomRarity()
    items = list(Card.objects.filter(rarity=rar))
    item = random.choice(items)
    return item


def getRandomAnimeCard(anime):
    items = Card.objects.filter(group__name=anime)
    rarity_list = items.values_list("rarity_id", "rarity__chance").distinct()
    rar = getRandomRarityWithList(rarity_list)
    items = list(items.filter(rarity=rar))
    item = random.choice(items)
    return item


def getRandomRarityWithList(list):
    maxchance = 0
    for rarity in list:
        maxchance += rarity[1]
    rand = random.randint(0, maxchance)
    for rarity in list:
        if rand <= rarity[1]:
            return int(rarity[0])
        else:
            rand -= rarity[1]


def getRandomRarity():
    maxchance = 0
    for rarity in Rarity.objects.all():
        maxchance += rarity.chance
    rand = random.randint(0, maxchance)
    for rarity in Rarity.objects.all():
        if rand < rarity.chance:
            return rarity.id
        else:
            rand -= rarity.chance


def getRandomCard2():
    rar = getRandomRarity2()
    items = list(Card.objects.filter(rarity=rar))
    item = random.choice(items)
    return item


def getRandomRarity2():
    maxchance = 0
    for rarity in Rarity.objects.exclude(name="Common"):
        maxchance += rarity.chance
    rand = random.randint(0, maxchance)
    for rarity in Rarity.objects.all():
        if rand < rarity.chance:
            return rarity.id
        else:
            rand -= rarity.chance
