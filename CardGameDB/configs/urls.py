from django.urls import path

from .views import CommonEmojisViewSet, EmbedViewSet


urlpatterns = [
    path(
        "commonemojis",
        CommonEmojisViewSet.as_view({"get": "list"}),
        name="Common Emojis",
    ),
    path(
        "embeds",
        EmbedViewSet.as_view({"get": "list"}),
        name="Common Emojis",
    )
]
