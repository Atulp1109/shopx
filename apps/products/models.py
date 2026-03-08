from django.db import models
from apps.stores.models import Store


class Category(models.Model):

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["store", "slug"]

    def __str__(self):
        return self.name



class Product(models.Model):

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField()

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["store", "slug"]

    def __str__(self):
        return self.name




class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="product_images/")

    alt_text = models.CharField(max_length=255, blank=True)

class ProductOption(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
    
class ProductOptionValue(models.Model):

    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value
    
class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    sku = models.CharField(max_length=100, unique=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.IntegerField(default=0)

    option_values = models.ManyToManyField(ProductOptionValue)

    def __str__(self):
        return self.sku