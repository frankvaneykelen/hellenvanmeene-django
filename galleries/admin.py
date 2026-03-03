from django.contrib import admin
from .models import Gallery


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["name", "place", "website", "sortorder", "do_not_show"]
    list_editable = ["sortorder", "do_not_show"]
    list_filter = ["do_not_show", "place__country"]
    search_fields = ["name", "description", "place__label"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["place"]
    fieldsets = (
        (None, {
            "fields": ("slug", "name", "place", "sortorder", "do_not_show"),
        }),
        ("Content", {
            "fields": ("description", "website", "phone", "phone2"),
        }),
        ("Image", {
            "fields": ("image_link", "image_alt"),
        }),
    )
