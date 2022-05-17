import uuid

from assets.asset_codes import ASSET_CODE_TYPE_CHOICES, AssetCodeType
from django.core.exceptions import ValidationError
from django.db import models

from .asset import Asset


class AssetCode(models.Model):
    """An individual code demarking an asset.."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    code = models.CharField(max_length=30, unique=True)
    code_type = models.CharField(max_length=1, choices=ASSET_CODE_TYPE_CHOICES)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.code

    def clean(self):
        try:
            code_type = AssetCodeType(self.code_type).get_strategy()
            code_type.validate(self.code)
        except KeyError:
            # This is theoretically unreachable, but it's good to be explicit.
            raise ValidationError(f"{self.code_type} is not a valid asset code type.")  # pragma: nocover
