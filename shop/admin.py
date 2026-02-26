from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "show"]
    list_filter = ["show"]
    search_fields = ["title", "description"]
    list_editable = ["show"]

