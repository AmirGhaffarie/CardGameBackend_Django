from .models import Emoji
from rest_framework.serializers import ModelSerializer


class CommonEmojisSerializer(ModelSerializer):
    class Meta:
        model = Emoji
        fields = ["name", "emoji"]
