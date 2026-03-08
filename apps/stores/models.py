from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Store(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores"
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    logo = models.ImageField(upload_to="store_logos/", blank=True, null=True)

    currency = models.CharField(max_length=10, default="USD")

    country = models.CharField(max_length=100, blank=True)

    timezone = models.CharField(max_length=100, default="UTC")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def domain(self):
        return f"{self.slug}.{settings.PLATFORM_DOMAIN}"