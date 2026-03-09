from rest_framework.routers import DefaultRouter, path
from .views import (
    CustomerViewSet,
    AddressViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
    OrderItemViewSet,
    CheckoutView
)

router = DefaultRouter()

router.register("profile", CustomerViewSet, basename="customer-profile")
router.register("addresses", AddressViewSet, basename="addresses")
router.register("carts", CartViewSet, basename="carts")
router.register("cart-items", CartItemViewSet, basename="cart-items")
router.register("orders", OrderViewSet, basename="orders")
router.register("order-items", OrderItemViewSet, basename="order-items")

urlpatterns = router.urls

urlpatterns = router.urls + [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
]