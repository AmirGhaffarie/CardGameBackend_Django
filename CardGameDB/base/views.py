from CardGameTestDB.game_configs import *
from datetime import timedelta, datetime, timezone
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Group, Card, Cooldowns, Inventory, Player, Rarity
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
    return HttpResponse(cd.get_all_cooldowns())


def balance(request, id):
    player = get_object_or_404(Player, userID=id)
    return HttpResponse(player.carrots)


def claim(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    cd.lastClaim = datetime.now(timezone.utc)
    cd.save()
    return HttpResponse(content="Success")


def drop(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    cooldown = cd.gacha_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    else:
        cd.lastDrop = datetime.now(timezone.utc)
        cd.save()
        return HttpResponse(get_random_card("900"))


def daily(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    cooldown = cd.daily_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    else:
        cd.lastDaily = datetime.now(timezone.utc)
        cd.save()
        return HttpResponse(get_random_card("300"))


def weekly(request, id, group):
    cd = get_object_or_404(Cooldowns, user=id)
    cooldown = cd.weekly_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    elif Group.objects.filter(name=group).exists():
        cd.lastWeekly = datetime.now(timezone.utc)
        cd.save()
        recs = []
        dic = {}
        for i in range(0, 2):
            recs.append(get_random_group_card(group, "300"))
        dic["res"] = recs
        return JsonResponse(dic)
    else:
        return HttpResponse(status=220, content="Group you entered not Exists")


def epicdrop(request, id):
    cd = get_object_or_404(Cooldowns, user=id)
    cooldown = cd.lucky_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    else:
        cd.lastEpicDrop = datetime.now(timezone.utc)
        cd.save()
        recs = []
        dic = {}
        for i in range(0, 3):
            recs.append(get_random_card("300"))
        dic["res"] = recs
        return JsonResponse(dic)


def gift_card(request, id_from, id_to, cardid):
    user_from = get_object_or_404(Player, userID=id_from)
    user_to = get_object_or_404(Player, userID=id_to)
    inv = get_object_or_404(Inventory, user=user_from, cardUID=cardid)
    inv.user = user_to
    inv.save()
    return HttpResponse("Success")


def check_having_cards(request, id, cardid):
    user = get_object_or_404(Player, userID=id)
    inv = get_object_or_404(Inventory, cardUID=cardid)
    return HttpResponse("Success")


def addcard(request, id, cardid, rarity):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=cardid)
    content = Inventory.objects.filter(user=user, card=card).exists()
    xp = Rarity.get_by_index(rarity).level * XP_PER_LEVEL
    inv = Inventory.objects.create(user=user, card=card, xp=xp)
    inv.save()
    return HttpResponse(content=content)

def checkduplicate(request, id, cardid):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=cardid)
    content = Inventory.objects.filter(user=user, card=card).exists()
    return HttpResponse(content=content)

def change_balance(request, id, amount):
    user = get_object_or_404(Player, userID=id)
    if (user.carrots + amount) >= 0:
        user.carrots += amount
        user.save()
        return HttpResponse(content="Success")
    else:
        return HttpResponse(status=210, content="Not enough money")


def viewcard(request, cardid):
    inv = get_object_or_404(Inventory, cardUID=cardid)
    card = inv.get_view_json()
    return HttpResponse(content=card)


def fuse(request, userid, main_card, feed_card):
    user = get_object_or_404(Player, userID=userid)
    main = get_object_or_404(Inventory, user=user, cardUID=main_card)
    feed = get_object_or_404(Inventory, user=user, cardUID=feed_card)
    similarities = 0
    if main.card.group == feed.card.group:
        similarities += 1
        if main.card.idol == feed.card.idol:
            similarities += 2
        if main.card.era == feed.card.era:
            similarities += 1
    xp = XP_PER_SIMILARITY[similarities]
    rarity_difference = (
        Rarity.get_from_xp(feed.xp).get_index()
        - Rarity.get_from_xp(main.xp).get_index()
    )
    xp *= XP_MULTIPLIER[rarity_difference]

    main.xp += xp
    main.save()
    feed.delete()

    return HttpResponse(xp)


class InventoryView(ListAPIView):
    def get(self, request, id, format=None):
        res = Inventory.objects.filter(user=id).order_by("card__group__name")
        paginator = InventoryPaginaiton()
        pag = paginator.paginate_queryset(res, request)
        invs = InventorySerializer(pag, many=True)
        pag = paginator.get_paginated_response(invs.data)
        return pag


# utils
def get_random_card(geometry):
    item: Card = Card.get_random()
    rarity: Rarity = Rarity.get_random().get_index()
    return item.get_json(rarity, geometry)


def get_random_group_card(group, geometry):
    item: Card = Card.get_random_from_group(group)
    rarity: Rarity = Rarity.get_random().get_index()
    return item.get_json(rarity, geometry)
