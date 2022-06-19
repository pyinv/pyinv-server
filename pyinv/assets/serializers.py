from rest_framework import serializers

from .models import Asset, AssetModel, Manufacturer, Node, NodeType


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for Asset objects."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node = serializers.PrimaryKeyRelatedField(read_only=True)
    asset_model = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    asset_codes = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    extra_data = serializers.JSONField(default=dict, required=False)

    class Meta:
        model = Asset
        fields = (
            'id',
            'node',
            'asset_model',
            'asset_codes',
            'first_asset_code',
            'state',
            'created_at',
            'updated_at',
            'extra_data',
        )


class ManufacturerLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a manufacturer."""

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug')


class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for Manufacturer."""
    asset_models = serializers.SlugRelatedField(source="assetmodel_set", slug_field="slug", read_only=True, many=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Manufacturer
        fields = ('name', 'slug', 'created_at', 'updated_at', 'asset_models')


class AssetModelSerializer(serializers.ModelSerializer):
    """Serializer for AssetModel objects."""
    manufacturer = ManufacturerLinkSerializer(read_only=True)

    class Meta:
        model = AssetModel
        fields = ('name', 'slug', 'manufacturer', 'is_container', 'created_at', 'updated_at', )


class NodeLinkSerializer(serializers.ModelSerializer):
    """Serializer with enough information to link to a node."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    is_container = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = Node
        fields = ('id', 'node_type', 'display_name', 'is_container')


class NodeSerializer(serializers.ModelSerializer):
    """Serializer for nodes."""

    id = serializers.UUIDField(read_only=True)  # noqa: A003
    name = serializers.CharField()
    node_type = serializers.ChoiceField(choices=NodeType.choices)
    asset = AssetSerializer()
    display_name = serializers.CharField(read_only=True)
    ancestors = serializers.ListField(child=NodeLinkSerializer(), read_only=True)
    is_container = serializers.BooleanField(read_only=True)

    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    numchild = serializers.IntegerField(read_only=True)
    depth = serializers.IntegerField(read_only=True)

    class Meta:
        model = Node
        fields = (
            'id',
            'name',
            'node_type',
            'asset',
            'display_name',
            'parent',
            'numchild',
            'depth',
            'ancestors',
            'is_container',
        )
