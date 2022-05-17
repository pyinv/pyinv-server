import uuid

from autoslug import AutoSlugField
from django.db import models


class Manufacturer(models.Model):
    """An entity that manufactures goods."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    name = models.CharField(max_length=30)
    slug = AutoSlugField(
        null=True,
        default=None,
        unique=True,
        editable=True,
        populate_from='name',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
