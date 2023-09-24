from django.contrib import admin
from base.models import *
# Register your models here.


class ChangeCheckAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'base/js/filter.js',   # inside app static folder
        )


admin.site.register(Player)
admin.site.register(Card, ChangeCheckAdmin)
admin.site.register(Inventory)
admin.site.register(Group)
admin.site.register(Idol)
admin.site.register(Era)
admin.site.register(Cooldown)
admin.site.register(Rarity)
