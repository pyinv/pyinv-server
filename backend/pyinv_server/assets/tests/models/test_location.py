from assets.models import Asset, AssetModel, Location, Manufacturer
from django.forms import ValidationError
from django.test import TestCase


class TestALocationModel(TestCase):

    def setUp(self) -> None:
        """Set up the test."""
        self.location = Location(name="world")
        self.location.save()
        self.manufacturer = Manufacturer(name="foo")
        self.manufacturer.save()
        self.asset_model = AssetModel(name="bar", manufacturer=self.manufacturer)
        self.asset_model.save()
        self.asset_model_container = AssetModel(
            name="bar", manufacturer=self.manufacturer, is_container=True,
        )
        self.asset_model_container.save()
        self.asset = Asset(name="foo", asset_model=self.asset_model, location=self.location)
        self.asset.save()
        self.container = Asset(name="foo", asset_model=self.asset_model_container, location=self.location)
        self.container.save()

    def test_create_location_in_root(self) -> None:
        """Test that we can create a location in root."""
        location = Location(name="bees")
        location.clean()
        location.save()

    def test_create_location_in_location(self) -> None:
        """Test that we can create a location in another location."""
        location = Location(name="bees", parent=self.location)
        location.clean()
        location.save()

    def test_create_very_nested_location(self) -> None:
        """Test that we can create a very deeply nested location."""
        loc = self.location
        for n in range(100):
            loc = Location(name=f"bees{n}", parent=loc)
            loc.clean()
            loc.save()

    def test_create_location_with_same_name(self) -> None:
        """Test that we can create a location with the same name."""
        location = Location(name="bees", parent=self.location)
        location.clean()
        location.save()
        location = Location(name="bees", parent=self.location)
        location.clean()
        location.save()

    def test_find_location_by_name(self) -> None:
        """Test that we can find a location by name."""
        location = Location.objects.get(name="world")
        self.assertEqual(location.name, "world")

    def test_find_location_by_name_in_location(self) -> None:
        """Test that we can find a location by name in a location."""
        location = Location.objects.get(name="world", parent=None)
        self.assertEqual(location.name, "world")

    def test_find_locations_in_root(self) -> None:
        """Test that we can find locations in root."""
        locations = Location.objects.filter(parent=None)
        self.assertEqual(len(locations), 1)

    def test_create_location_linked_asset(self) -> None:
        """Test that we can create a location linked to an asset."""
        loc = Location(parent=self.location, asset=self.container)
        loc.clean()

    def test_create_location_linked_asset_not_container(self) -> None:
        """Test that we cannot create a location linked to an asset that is not a container."""
        with self.assertRaises(ValidationError):
            loc = Location(parent=self.location, asset=self.asset)
            loc.clean()

    def test_create_location_linked_asset_not_name(self) -> None:
        """Test that we cannot create a location linked to an asset with a name."""
        with self.assertRaises(ValidationError):
            loc = Location(name="bee", parent=self.location, asset=self.container)
            loc.clean()

    def test_location_str_unlinked(self) -> None:
        """Test the __str__ of an unlinked location."""
        location = Location(name="bees")
        self.assertEqual(str(location), "Location: bees")

    def test_location_str_linked(self) -> None:
        """Test the __str__ of a linked location."""
        location = Location(asset=self.container)
        self.assertRegexpMatches(str(location), "Asset: foo.*")

    def test_location_unlinked_must_have_name(self) -> None:
        """Test that an unlinked location must have a name."""
        location = Location()
        with self.assertRaises(ValidationError):
            location.clean()

    def test_unlinked_location_cannot_be_within_linked(self) -> None:
        """Test that an unlinked location cannot be within a linked location."""
        location = Location(name="bees", parent=self.location, asset=self.asset)
        location.save()
        with self.assertRaises(ValidationError):
            location.clean()
