from assets.models import AssetModel, Manufacturer
from django.db.models.deletion import ProtectedError
from django.test import TestCase


class TestAssetModel(TestCase):

    def setUp(self):
        super().setUp()
        self.manufacturer = Manufacturer.objects.create(name="BeeCorp")
        self.container = AssetModel.objects.create(
            name="Hive",
            is_container=True,
            manufacturer=self.manufacturer,
        )
        self.not_container = AssetModel.objects.create(
            name="Honey Pot",
            is_container=False,
            manufacturer=self.manufacturer,
        )

    def test_set_slug_automatically(self) -> None:
        """Test that the slug is set automatically."""
        self.assertEqual(self.container.slug, "hive")
        self.assertEqual(self.not_container.slug, "honey-pot")

    def test_str(self) -> None:
        self.assertEqual(str(self.container), "BeeCorp Hive")

    def test_protected_from_manufacturer_delete(self) -> None:
        """Test that deleting the manager does not casade."""
        with self.assertRaisesRegex(ProtectedError, "BeeCorp Hive"):
            self.manufacturer.delete()
