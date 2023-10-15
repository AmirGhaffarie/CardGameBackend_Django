from django.contrib import admin
from base.models import *
# Register your models here.


class IdolInline(admin.TabularInline):
    model = Idol
    extra = 0


class EraInline(admin.TabularInline):
    model = Era
    extra = 0


class GroupAdmin(admin.ModelAdmin):
    inlines = [IdolInline, EraInline]


admin.site.register(Player)
admin.site.register(Card)
admin.site.register(Inventory)
admin.site.register(Group, GroupAdmin)
admin.site.register(Idol)
admin.site.register(Era)
admin.site.register(Cooldown)
admin.site.register(Rarity)
