from .models import Emoji, Embed
from rest_framework.serializers import ModelSerializer


class CommonEmojisSerializer(ModelSerializer):
    class Meta:
        model = Emoji
        fields = ["name", "emoji"]


class EmbedSerializer(ModelSerializer):
    class Meta:
        model = Embed
        fields = ["name", "embed"]
