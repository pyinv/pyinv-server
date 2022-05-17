from assets.models import Asset, AssetCode, AssetModel, Location, Manufacturer
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase


class TestAssetCodeModel(TestCase):

    def setUp(self) -> None:
        """Set up the test."""
        self.location = Location(name="bees")
        self.location.save()
        self.manufacturer = Manufacturer(name="foo")
        self.manufacturer.save()
        self.asset_model = AssetModel(name="bar", manufacturer=self.manufacturer)
        self.asset_model.save()
        self.asset = Asset(name="foo", asset_model=self.asset_model, location=self.location)
        self.asset.save()

    def test_no_duplicate_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo", asset=self.asset)
        code.save()
        code2 = AssetCode(code_type="A", code="foo", asset=self.asset)

        with self.assertRaises(IntegrityError):
            code2.save()

    def test_arbitrary_code(self) -> None:
        """Test that we can make a arbitrary asset code."""
        code = AssetCode(code_type="A", code="foo", asset=self.asset)
        self.assertEqual(code.code, "foo")

    def test_validate_damm32(self) -> None:
        """Test that we can create a valid damm32 code."""
        code = AssetCode(code_type="D", code="INV-ASE-SEJ", asset=self.asset)
        code.full_clean()

    def test_validate_damm32_bad_check_digit(self) -> None:
        """Test that we catch a bad check digit."""
        code = AssetCode(code_type="D", code="INV-ASE-SEU", asset=self.asset)
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_invalid_damm32_format(self) -> None:
        """Test that we catch a bad damm32 format."""
        code = AssetCode(code_type="D", code="foo", asset=self.asset)
        with self.assertRaises(ValidationError):
            code.full_clean()

    def test_invalid_format(self) -> None:
        """Test that we catch a non-existent format."""
        code = AssetCode(code_type="?", code="foo", asset=self.asset)
        with self.assertRaises(ValueError):
            code.full_clean()
