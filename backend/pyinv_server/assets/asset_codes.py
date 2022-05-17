from abc import ABC, abstractmethod
from enum import Enum
from random import choice
from re import compile
from typing import Dict, List, Optional, Tuple

from damm32 import BadCharacterException, Damm32
from django.conf import settings
from django.core.exceptions import ValidationError


class AssetCodeStrategy(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the asset code type."""
        raise NotImplementedError  # pragma: nocover

    def generate_new_code(self) -> Optional[str]:
        """
        Generate a new asset code.
        :returns: New, unused asset code or None if could not generate
        """
        return None  # pragma: nocover

    @abstractmethod
    def validate(self, asset_code: str) -> None:
        """
        Validate an asset code.
        :param asset_code: Asset Code to validate.
        :raises django.core.exceptions.ValidationError: The asset code was invalid.
        """
        raise NotImplementedError  # pragma: nocover


class ArbitraryStringAssetCodeStrategy(AssetCodeStrategy):

    name = "Arbitrary String"

    def validate(self, asset_code: str) -> None:
        """
        Validate an asset code.
        :param asset_code: Asset Code to validate.
        :raises django.core.exceptions.ValidationError: The asset code was invalid.
        """
        if len(asset_code) == 0:
            raise ValidationError("Asset code must be at least character long")


class Damm32AssetCodeStrategy(AssetCodeStrategy):

    name = "Damm 32"

    ASSET_CODE_REGEX = compile(r"^([A-Za-z0-9]{3})-([A-Za-z0-9]{3})-([A-Za-z0-9]{3})$")

    def __init__(self) -> None:
        self._d32 = Damm32()
        self._alphabet = self._d32._alphabet
        self._default_prefix = settings.DAMM32_ASSET_CODE_DEFAULT_PREFIX
        self._allowed_prefixes = settings.DAMM32_ASSET_CODE_PREFIXES

    def generate_new_code(self) -> Optional[str]:
        """
        Generate a new asset code.
        :returns: New, unused asset code or None if could not generate
        """
        code = self._default_prefix + "".join(choice(self._alphabet) for _ in range(5))
        code += self._d32.calculate(code)

        return f"{code[:3]}-{code[3:6]}-{code[6:9]}"

    def validate(self, asset_code: str) -> None:
        """
        Validate an asset code.
        :param asset_code: Asset Code to validate.
        :raises django.core.exceptions.ValidationError: The asset code was invalid.
        """
        match = self.ASSET_CODE_REGEX.match(asset_code)

        if match:
            e = "".join(match.groups())
            try:
                if not self._d32.verify(e.upper()):
                    raise ValidationError(
                        f"Invalid asset code check digit. {self._d32.calculate(e[:8])}"
                    )
            except BadCharacterException:
                bad_chars = ", ".join({c for c in e if c not in self._alphabet})
                raise ValidationError(
                    f"Invalid characters in code: {bad_chars}",
                )

            # Check that the prefix is allowed by the settings
            if e[:3] not in self._allowed_prefixes:
                raise ValidationError(f"Invalid asset code prefix: {e[:3]}")
        else:
            raise ValidationError(f"Invalid asset code format: {asset_code}")


class AssetCodeType(str, Enum):
    """Available Asset Code Types."""

    ARBITRARY = "A"
    DAMM32 = "D"

    @classmethod
    def strategy_mapping(cls) -> Dict['AssetCodeType', AssetCodeStrategy]:
        """Mapping of code types to strategies."""
        return {
            AssetCodeType.ARBITRARY: ArbitraryStringAssetCodeStrategy(),
            AssetCodeType.DAMM32: Damm32AssetCodeStrategy(),
        }

    def get_strategy(self) -> AssetCodeStrategy:
        return self.strategy_mapping()[self]


ASSET_CODE_TYPE_CHOICES: List[Tuple[str, AssetCodeType]] = [
    (key.value, code_type.name)
    for key, code_type in AssetCodeType.strategy_mapping().items()
]
