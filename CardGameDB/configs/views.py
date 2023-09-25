from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CommonEmojisSerializer, EmbedSerializer
from .models import Emoji, Embed

# Create your views here.


class CommonEmojisViewSet(viewsets.ModelViewSet):
    queryset = Emoji.objects.all()
    serializer_class = CommonEmojisSerializer


class EmbedViewSet(viewsets.ModelViewSet):
    queryset = Embed.objects.all()
    serializer_class = EmbedSerializer
