from django.contrib import admin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect

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


class CardModelAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                super().save_model(request, obj, form, change)
        except IntegrityError:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Duplicate card ID.either you\'re creating a duplicate card or having the same '
                                    + 'short name on groups, eras or idols.')
            # Prevents saving the model and redirects back to the change form
            return HttpResponseRedirect('.')


admin.site.register(Player)
admin.site.register(Card, CardModelAdmin)
admin.site.register(Inventory)
admin.site.register(Group, GroupAdmin)
admin.site.register(Idol)
admin.site.register(Era)
admin.site.register(Cooldown)
admin.site.register(Rarity)
