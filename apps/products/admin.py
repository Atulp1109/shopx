from django.contrib import admin

from .models import Category,Product,ProductImage,ProductOption,ProductOptionValue,ProductVariant
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductOption)
admin.site.register(ProductOptionValue)
admin.site.register(ProductVariant)