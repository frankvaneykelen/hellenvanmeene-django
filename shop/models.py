"""Shop — placeholder. Expand when shop requirements are defined."""

from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_link = models.CharField(max_length=500, blank=True, default="")
    show = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ShopProducts"
        ordering = ["title"]

    def __str__(self):
        return self.title

