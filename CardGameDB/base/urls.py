from django.urls import register_converter, path
from . import views, converters

register_converter(converters.SignedInt, "signedint")

urlpatterns = [
    path("register/<int:id>", views.register, name="Register"),
    path("cds/<int:id>", views.cds, name="Cooldowns"),
    path("claim/<int:id>", views.claim, name="Claim"),
    path("stargaze/<int:id>", views.stargaze, name="SG"),
    path("discover/<int:id>", views.discover, name="DC"),
    path("drop/<int:id>", views.drop, name="Drop"),
    path("daily/<int:id>", views.daily, name="Daily"),
    path("weekly/<int:id>/<path:group>", views.weekly, name="Weekly"),
    path("epicdrop/<int:id>", views.epic_drop, name="EpicDrop"),
    path("addcard/<int:id>/<path:card_id>", views.add_card, name="AddCard"),
    path("checkduplicate/<int:id>/<path:card_id>", views.check_duplicate, name="CheckDuplicate"),
    path(
        "checkcard/<int:id>/<path:card_id>",
        views.check_having_cards,
        name="CheckCards",
    ),
    path(
        "giftcard/<int:id_from>/<int:id_to>/<path:card_id>",
        views.gift_card,
        name="GiftCard",
    ),
    path(
        "changebalance/<int:id>/<signedint:amount>",
        views.change_balance,
        name="ChangeBalance",
    ),
    path("balance/<int:id>/", views.balance, name="Balance"),
    path("inventory/<int:id>", views.InventoryView.as_view(), name="Inventory"),
    path("viewcard/<path:card_id>", views.view_card, name="View"),
    path("eracount/<int:id>/<path:era>", views.era_count, name="Era Count"),
    path('get_idols/', views.get_idols, name='get_idols'),
    path('get_eras/', views.get_eras, name='get_eras')
]
