from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import (
    Product,
    Category,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    ProductImage,
)

from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ProductOptionSerializer,
    ProductOptionValueSerializer,
    ProductVariantSerializer,
    ProductImageSerializer,
)

from apps.stores.models import Store

class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(store__owner=self.request.user)

    def perform_create(self, serializer):
        store_id = self.request.data.get("store")

        store = Store.objects.get(
            id=store_id,
            owner=self.request.user
        )

        serializer.save(store=store)


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(store__owner=self.request.user)

    def perform_create(self, serializer):
        store_id = self.request.data.get("store")

        store = Store.objects.get(
            id=store_id,
            owner=self.request.user
        )

        serializer.save(store=store)

class ProductOptionViewSet(ModelViewSet):

    queryset = ProductOption.objects.all()
    serializer_class = ProductOptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductOption.objects.filter(
            product__store__owner=self.request.user
        )
    
class ProductOptionValueViewSet(ModelViewSet):

    queryset = ProductOptionValue.objects.all()
    serializer_class = ProductOptionValueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductOptionValue.objects.filter(
            option__product__store__owner=self.request.user
        )

class ProductVariantViewSet(ModelViewSet):

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductVariant.objects.filter(
            product__store__owner=self.request.user
        )


class ProductImageViewSet(ModelViewSet):

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProductImage.objects.filter(
            product__store__owner=self.request.user
        )