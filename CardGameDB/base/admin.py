from django.contrib import admin
from base.models import Player, Card, Inventory, AnimeSeries, Cooldowns, Rarity

# Register your models here.
admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Inventory)
admin.site.register(AnimeSeries)
admin.site.register(Cooldowns)
admin.site.register(Rarity)
