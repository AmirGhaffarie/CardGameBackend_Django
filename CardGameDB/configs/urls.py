from django.urls import path

from .views import CommonEmojisViewSet, EmbedViewSet, DiscoverViewSet


urlpatterns = [
    path(
        "commonemojis",
        CommonEmojisViewSet.as_view({"get": "list"}),
        name="Emojis",
    ),
    path(
        "embeds",
        EmbedViewSet.as_view({"get": "list"}),
        name="Embeds",
    ),
    path(
        "discover",
        DiscoverViewSet.as_view({"get": "list"}),
        name="Discovers",
    )
]
