from rest_framework.routers import DefaultRouter
from .views import StoreViewSet

router = DefaultRouter()
router.register("", StoreViewSet, basename="stores")

urlpatterns = router.urls