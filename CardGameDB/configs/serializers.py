from .models import CommonEmojis
from rest_framework.serializers import ModelSerializer


class CommonEmojisSerializer(ModelSerializer):
    class Meta:
        model = CommonEmojis
        fields = ["name", "emoji"]
