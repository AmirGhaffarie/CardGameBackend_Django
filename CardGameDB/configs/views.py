from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CommonEmojisSerializer
from .models import CommonEmojis

# Create your views here.


class CommonEmojisViewSet(viewsets.ModelViewSet):
    queryset = CommonEmojis.objects.all()
    serializer_class = CommonEmojisSerializer