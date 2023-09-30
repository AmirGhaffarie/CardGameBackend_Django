from datetime import datetime, timezone
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import Group, Card, Cooldown, Inventory, Player, PlayerEraCount, Era
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
    cd = get_object_or_404(Cooldown, user=id)
    return HttpResponse(cd.get_all_cooldowns())


def balance(request, id):
    player = get_object_or_404(Player, userID=id)
    return HttpResponse(player.carrots)


def claim(request, id):
    cd = get_object_or_404(Cooldown, user=id)
    cd.lastClaim = datetime.now(timezone.utc)
    cd.save()
    return HttpResponse(content="Success")


def drop(request, id):
    cd = get_object_or_404(Cooldown, user=id)
    cooldown = cd.gacha_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    else:
        cd.lastDrop = datetime.now(timezone.utc)
        cd.save()
        return HttpResponse(get_random_card("900"))


def daily(request, id):
    cd = get_object_or_404(Cooldown, user=id)
    cooldown = cd.daily_remaining_time()
    if cooldown.total_seconds() > 0:
        return HttpResponse(status=210, content=str(cooldown))
    else:
        cd.lastDaily = datetime.now(timezone.utc)
        cd.save()
        return HttpResponse(get_random_card("300"))


def weekly(request, id, group):
    cd = get_object_or_404(Cooldown, user=id)
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


def epic_drop(request, id):
    cd = get_object_or_404(Cooldown, user=id)
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


def gift_card(request, id_from, id_to, card_id):
    user_from = get_object_or_404(Player, userID=id_from)
    user_to = get_object_or_404(Player, userID=id_to)
    inv = get_object_or_404(Inventory, user=user_from, cardUID=card_id)
    inv.user = user_to
    inv.save()
    return HttpResponse("Success")


def check_having_cards(request, id, card_id):
    get_object_or_404(Player, userID=id)
    get_object_or_404(Inventory, cardUID=card_id)
    return HttpResponse("Success")


def add_card(request, id, card_id):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=card_id)
    content = Inventory.objects.filter(user=user, card=card).exists()
    inv = Inventory.objects.create(user=user, card=card)
    inv.save()
    pec, exist = PlayerEraCount.objects.get_or_create(user=user, card=card)
    pec.count = Inventory.objects.filter(user=user, card__era=card.era).count()
    pec.save()
    return HttpResponse(content=content)


def check_duplicate(request, id, card_id):
    user = get_object_or_404(Player, userID=id)
    card = get_object_or_404(Card, cardUID=card_id)
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


def view_card(request, card_id):
    inv = get_object_or_404(Inventory, cardUID=card_id)
    card = inv.get_view_json()
    return HttpResponse(content=card)


class InventoryView(ListAPIView):
    def get(self, request, id):
        res = (Inventory.objects.filter(user=id).order_by("card__group__name"))
        if 'group' in request.GET:
            res = res.filter(card__group__name=request.GET.get('group'))
        if 'era' in request.GET:
            res = res.filter(card__era__name=request.GET.get('era'))
        if 'idol' in request.GET:
            res = res.filter(card__idol__name=request.GET.get('idol'))
        paginator = InventoryPaginaiton()
        pag = paginator.paginate_queryset(res, request)
        invs = InventorySerializer(pag, many=True)
        pag = paginator.get_paginated_response(invs.data)
        return pag


def era_count(request, id, era):
    q = Era.objects.filter(name=era)
    if not q.exists():
        return 0
    found_era = q.first()
    pec, created = PlayerEraCount.objects.get_or_create(user_id=id, era=found_era)
    if created:
        pec.count = Inventory.objects.filter(user_id=id, card__era=found_era).count()
        pec.save()
    return pec.count


# utils
def get_random_card(geometry):
    item: Card = Card.get_random()
    return item.get_json(geometry)


def get_random_group_card(group, geometry):
    item: Card = Card.get_random_from_group(group)
    return item.get_json(geometry)


