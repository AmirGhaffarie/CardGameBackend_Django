from django.contrib import admin
from django import forms
from base.models import Player, Card, Inventory, Group, Cooldowns, Rarity, Era, Idol

# Register your models here.


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = "__all__"


class CardAdmin(admin.ModelAdmin):
    form = CardForm


admin.site.register(Player)
admin.site.register(Card, CardAdmin)
admin.site.register(Inventory)
admin.site.register(Group)
admin.site.register(Idol)
admin.site.register(Era)
admin.site.register(Cooldowns)
admin.site.register(Rarity)
