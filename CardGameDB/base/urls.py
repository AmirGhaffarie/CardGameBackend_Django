from django.urls import register_converter, path
from . import views, converters

register_converter(converters.SignedInt, "signedint")

urlpatterns = [
    path("register/<int:id>", views.register, name="Register"),
    path("cds/<int:id>", views.cds, name="Cooldowns"),
    path("claim/<int:id>", views.claim, name="Claim"),
    path("drop/<int:id>", views.drop, name="Drop"),
    path("daily/<int:id>", views.daily, name="Daily"),
    path("weekly/<int:id>/<path:group>", views.weekly, name="Weekly"),
    path("epicdrop/<int:id>", views.epic_drop, name="EpicDrop"),
    path("addcard/<int:id>/<card_id>", views.add_card, name="AddCard"),
    path("checkduplicate/<int:id>/<card_id>", views.check_duplicate, name="CheckDuplicate"),
    path(
        "checkcard/<int:id>/<card_id>",
        views.check_having_cards,
        name="CheckCards",
    ),
    path(
        "giftcard/<int:id_from>/<int:id_to>/<card_id>",
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
    path("viewcard/<card_id>", views.view_card, name="View")
]
