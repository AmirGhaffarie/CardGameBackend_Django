from django.urls import path

from .views import CommonEmojisViewSet


urlpatterns = [
    path(
        "commonemojis",
        CommonEmojisViewSet.as_view({"get": "list"}),
        name="Common Emojis",
    )
]
