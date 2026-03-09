from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    StorefrontStoreView,
    StorefrontProductViewSet,
    StorefrontCategoryViewSet
)

router = DefaultRouter()

router.register("products", StorefrontProductViewSet, basename="storefront-products")
router.register("categories", StorefrontCategoryViewSet, basename="storefront-categories")

urlpatterns = [
    path("store/", StorefrontStoreView.as_view()),
]

urlpatterns += router.urls