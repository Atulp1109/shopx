from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.stores.models import Store
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer


class StorefrontStoreView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        store = request.store

        if not store:
            return Response(
                {"detail": "Store not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "id": store.id,
            "name": store.name,
            "slug": store.slug,
            "logo": store.logo.url if store.logo else None,
            "domain": store.domain,
        }

        return Response(data)


class StorefrontCategoryViewSet(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):

        store = self.request.store

        if not store:
            return Category.objects.none()

        return Category.objects.filter(store=store)


class StorefrontProductViewSet(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_fields = ["category"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):

        store = self.request.store

        if not store:
            return Product.objects.none()

        return Product.objects.filter(
            store=store,
            is_active=True
        ).select_related(
            "category"
        ).prefetch_related(
            "variants",
            "images",
            "options"
        )