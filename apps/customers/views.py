from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer, Address, Cart, CartItem, Order, OrderItem
from .serializers import (
    CustomerSerializer,
    AddressSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CheckoutSerializer
)

from apps.products.models import ProductVariant
from apps.stores.models import Store

class CustomerViewSet(ModelViewSet):

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressViewSet(ModelViewSet):

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):

        customer = Customer.objects.get(user=self.request.user)

        serializer.save(customer=customer)

class CartViewSet(ModelViewSet):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):

        customer = Customer.objects.get(user=self.request.user)

        serializer.save(customer=customer)

class CartItemViewSet(ModelViewSet):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)
    
class OrderViewSet(ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):

        customer = Customer.objects.get(user=self.request.user)

        serializer.save(customer=customer)

class OrderItemViewSet(ModelViewSet):

    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(
            order__customer__user=self.request.user
        )
    
class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = serializer.validated_data["cart_id"]
        address_id = serializer.validated_data["address_id"]

        customer = Customer.objects.get(user=request.user)

        cart = Cart.objects.get(
            id=cart_id,
            customer=customer,
            is_active=True
        )

        address = Address.objects.get(
            id=address_id,
            customer=customer
        )

        cart_items = cart.items.all()

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            customer=customer,
            store=cart.store,
            status="PENDING",
            total_amount=0
        )

        total = 0

        for item in cart_items:

            variant = item.variant

            if variant.stock < item.quantity:
                return Response(
                    {"detail": f"{variant.sku} out of stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            variant.stock -= item.quantity
            variant.save()

            price = variant.price * item.quantity
            total += price

            OrderItem.objects.create(
                order=order,
                variant=variant,
                price=variant.price,
                quantity=item.quantity
            )

        order.total_amount = total
        order.save()

        cart.items.all().delete()
        cart.is_active = False
        cart.save()

        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "total_amount": total
            }
        )