import uuid

from django.core.exceptions import ValidationError
from django.db import models
from treebeard.al_tree import AL_Node

from .asset import Asset


class Location(AL_Node):
    """A location in the inventory."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    name = models.CharField(max_length=30, blank=True)
    parent = models.ForeignKey(
        'self',
        related_name='children_set',
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.PROTECT,
    )
    asset = models.OneToOneField(
        Asset,
        on_delete=models.PROTECT,
        related_name='linked_location',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    node_order_by = ['name']

    def __str__(self):
        if self.asset is None:
            return f'Location: {self.name}'
        else:
            return f'Asset: {self.asset}'

    def clean(self):
        if self.asset is not None:
            if not self.asset.asset_model.is_container:
                raise ValidationError('A location can only be assigned to an asset that is a container.')

            if self.asset.state != Asset.State.KNOWN:
                raise ValidationError('A location can only be assigned to an asset that is in a known state.')

            if self.name != "":
                raise ValidationError('A location cannot be assigned to an asset and have a name.')

            if self.asset.location != self.parent:
                raise ValidationError('A location can only be assigned to an asset that is in the same location.')
        else:
            if self.parent is not None and self.parent.asset is not None:
                raise ValidationError('A location cannot be within an asset.')

            if not self.name:
                raise ValidationError('A location must have a name or be assigned to an asset.')
