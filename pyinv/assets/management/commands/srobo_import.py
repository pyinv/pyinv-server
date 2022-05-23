from json import loads
from pathlib import Path
from typing import List

from assets.models import (
    Asset,
    AssetCode,
    AssetEvent,
    AssetModel,
    Changeset,
    Location,
    Manufacturer,
)
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import dateparse


class Command(BaseCommand):

    help = 'Import assets from Student Robotics JSON format'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('data_folder', type=Path)

    def get_asset_by_code(self, code) -> Asset:
        code = AssetCode.objects.get(code=code)
        return code.asset

    def get_location(self, ref) -> Location:
        try:
            parent_asset = self.get_asset_by_code(ref)
            if not parent_asset.asset_model.is_container:
                parent_asset.asset_model.is_container = True
                parent_asset.asset_model.save()
            location, _ = Location.objects.get_or_create(asset=parent_asset)
            return location
        except AssetCode.DoesNotExist:
            if ref.startswith("sr"):
                loc, _ = Location.objects.get_or_create(name="unknown")
                return loc
            else:
                parts = ref.split("/")
                return self.get_non_asset_location(parts)

    def get_non_asset_location(self, parts: List[str], parent=None) -> None:
        top_level = parts.pop(0)

        location, _ = Location.objects.get_or_create(name=top_level, parent=parent)

        if len(parts) > 0:
            return self.get_non_asset_location(parts, location)
        else:
            return location

    def handle(self, *args, **options):
        data_folder: Path = options['data_folder']
        self.stdout.write(f"Importing from {data_folder}")

        self._default_manufacturer, _ = Manufacturer.objects.get_or_create(name="Unknown")

        for file in sorted(data_folder.glob("*.yaml")):
            self.stdout.write(f"Processing {file}")
            data = loads(file.read_text())

            user, _ = User.objects.get_or_create(
                username=data['user'],
                email=data['user'],
                is_active=False,
            )

            cs = Changeset.objects.create(
                timestamp=dateparse.parse_datetime(data["timestamp"] + "Z"),
                user=user,
                comment=data["comment"],
            )

            for event in data["events"]:
                if event["event"] == "add":
                    self._handle_add_asset_event(cs, event)
                elif event["event"] == "move":
                    self._handle_move_asset_event(cs, event)

    def _handle_move_asset_event(self, cs, event) -> None:
        asset = self.get_asset_by_code(event["asset_code"])
        location = self.get_location(event["new_location"])
        asset.location = location
        asset.save()

        AssetEvent.objects.create(
            changeset=cs,
            event_type="M",
            asset=asset,
            data=event,
        )

    def _handle_add_asset_event(self, cs, event) -> None:
        asset_data = event["asset"]

        location = self.get_location(asset_data["location"])
        asset_model, _ = AssetModel.objects.get_or_create(
            name=asset_data["asset_type"],
            manufacturer=self._default_manufacturer,
        )

        asset = Asset.objects.create(
            asset_model=asset_model,
            state="K",
            location=location,
            extra_data=asset_data["data"],
        )

        try:
            AssetCode.objects.get_or_create(asset=asset, code=asset_data["asset_code"], code_type="A")
        except IntegrityError:
            print("WARNING: You have run the import multiple times!")

        AssetEvent.objects.create(
            changeset=cs,
            event_type="A",
            asset=asset,
            data=event,
        )
