import uuid

from autoslug import AutoSlugField
from django.db import models

from .manufacturer import Manufacturer


class AssetModel(models.Model):
    """The model of an asset."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    name = models.CharField(max_length=30)
    slug = AutoSlugField(
        null=True,
        default=None,
        unique=True,
        editable=True,
        populate_from='name',
    )
    is_container = models.BooleanField(default=False, verbose_name="Can contain assets")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.manufacturer.name} {self.name}"
