from rest_framework import viewsets

from .models import Asset, AssetModel, Location, Manufacturer
from .serializers import (
    AssetModelSerializer,
    AssetSerializer,
    LocationSerializer,
    ManufacturerSerializer,
)


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Assets to be viewed.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssetModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AssetModels to be viewed or edited.
    """
    queryset = AssetModel.objects.all()
    serializer_class = AssetModelSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Locations to be viewed.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows manufacturers to be viewed or edited.
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
