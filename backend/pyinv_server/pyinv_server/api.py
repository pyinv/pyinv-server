import assets.api
from rest_framework import routers

router = routers.DefaultRouter()
router.register('assets', assets.api.AssetViewSet)
router.register('locations', assets.api.LocationViewSet)
router.register('manufacturers', assets.api.ManufacturerViewSet)
router.register('models', assets.api.AssetModelViewSet)
