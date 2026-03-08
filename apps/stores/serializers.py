from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):

    domain = serializers.ReadOnlyField()

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "slug",
            "domain",
            "description",
            "logo",
            "currency",
            "country",
            "timezone",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "domain",
            "created_at",
            "updated_at",
        ]