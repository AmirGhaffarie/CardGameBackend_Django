from .models import Inventory
from rest_framework.serializers import ModelSerializer


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory

    def to_representation(self, instance):
        return instance.getInfo()
