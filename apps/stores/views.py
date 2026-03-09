from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from apps.users.permissions import IsMerchant
from .models import Store
from .serializers import StoreSerializer



class StoreViewSet(ModelViewSet):

    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsMerchant]
    parser_classes = [MultiPartParser, FormParser]
    def get_queryset(self):

        return Store.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)