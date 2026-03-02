from django import forms
from django.contrib import admin
from django.utils.html import format_html
from core.widgets import BlobURLWidget, EasyMDEWidget
from .models import Product, ShopProductTag, ShopProductType


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "description": EasyMDEWidget,
            "image_url": BlobURLWidget(
                container_url="https://hellenvanmeene.blob.core.windows.net/website-images"
            ),
        }

@admin.register(ShopProductType)
class ShopProductTypeAdmin(admin.ModelAdmin):
    search_fields = ["label"]


class ShopProductTagInline(admin.TabularInline):
    model = ShopProductTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    save_as = True
    list_display = ["title", "product_type", "price", "show"]
    list_filter = ["show", "product_type"]
    search_fields = ["title", "description"]
    list_editable = ["show"]
    autocomplete_fields = ["product_type", "currency"]
    readonly_fields = ["image_preview"]
    fieldsets = [
        (None, {"fields": ["title", "description", "price", "currency", "product_type", "shop_link", "show"]}),
        ("Image", {"fields": ["image_url", "image_preview"]}),
    ]
    inlines = [ShopProductTagInline]

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height:300px; max-width:100%; '
                'border-radius:4px; margin-top:6px;" />',
                obj.image_url,
            )
        return "—"

