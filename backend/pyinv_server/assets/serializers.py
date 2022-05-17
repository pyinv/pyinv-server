from rest_framework import serializers

from .models import Asset, AssetModel, Location, Manufacturer


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            "id",
            "name",
            "asset_model",
            "state",
            "linked_location",
            "location",
            "asset_codes",
            "created_at",
            "updated_at",
            "extra_data",
        ]


class AssetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetModel
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'
