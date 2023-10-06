from .models import Emoji, Embed, DiscoverItem
from rest_framework.serializers import ModelSerializer


class CommonEmojisSerializer(ModelSerializer):
    class Meta:
        model = Emoji
        fields = ["name", "emoji"]


class EmbedSerializer(ModelSerializer):
    class Meta:
        model = Embed
        fields = ["name", "embed"]


class DiscoverSerializer(ModelSerializer):
    class Meta:
        model = DiscoverItem
        fields = ["name", "chance", "amount", "description"]
