from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    ProductViewSet,
    CategoryViewSet,
    ProductOptionViewSet,
    ProductOptionValueViewSet,
    ProductVariantViewSet,
    ProductImageViewSet,
)

router = DefaultRouter()

router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("options", ProductOptionViewSet, basename="options")
router.register("option-values", ProductOptionValueViewSet, basename="option-values")
router.register("variants", ProductVariantViewSet, basename="variants")
router.register("images", ProductImageViewSet, basename="images")

urlpatterns = router.urls