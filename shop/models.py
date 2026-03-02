"""Shop — placeholder. Expand when shop requirements are defined."""

from django.db import models
from core.models import Currency, Tag


class ShopProductType(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "ShopProductTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Product(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products",
    )
    image_url = models.URLField(max_length=1000, blank=True, default="")
    product_type = models.ForeignKey(
        ShopProductType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products",
    )
    show = models.BooleanField(default=True)
    shop_link = models.URLField(max_length=1000, blank=True, default="")
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ShopProducts"
        ordering = ["title"]

    def __str__(self):
        return self.title


class ShopProductTag(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_tags",
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="product_tags",
    )

    class Meta:
        db_table = "ShopProductTags"
        unique_together = [("product", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.product}"

