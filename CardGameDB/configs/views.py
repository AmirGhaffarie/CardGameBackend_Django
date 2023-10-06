from rest_framework import viewsets
from .serializers import CommonEmojisSerializer, EmbedSerializer, DiscoverSerializer
from .models import Emoji, Embed, DiscoverItem

# Create your views here.


class CommonEmojisViewSet(viewsets.ModelViewSet):
    queryset = Emoji.objects.all()
    serializer_class = CommonEmojisSerializer


class EmbedViewSet(viewsets.ModelViewSet):
    queryset = Embed.objects.all()
    serializer_class = EmbedSerializer


class DiscoverViewSet(viewsets.ModelViewSet):
    queryset = DiscoverItem.objects.all()
    serializer_class = DiscoverSerializer
