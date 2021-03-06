from django.test import TestCase

from assets.models import Manufacturer


class TestManufacturerModel(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.bees = Manufacturer.objects.create(name="Bees")

    def test_manufacturer_set_slug_automatically(self) -> None:
        """Test that the slug is set automatically."""
        self.assertEqual(self.bees.slug, "bees")

    def test_str(self) -> None:
        self.assertEqual(str(self.bees), "Bees")
