from rest_framework import serializers
from .models import (
    Product,
    Category,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    ProductImage,
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductOptionValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionValue
        fields = "__all__"


class ProductOptionSerializer(serializers.ModelSerializer):

    values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    option_values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):

    variants = ProductVariantSerializer(many=True, read_only=True)
    options = ProductOptionSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["store"]