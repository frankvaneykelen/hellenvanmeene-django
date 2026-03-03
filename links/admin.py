from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["sortorder", "label", "url", "do_not_show"]
    list_editable = ["sortorder", "do_not_show"]
    list_display_links = ["label"]
    search_fields = ["label", "url", "description"]
    ordering = ["sortorder", "id"]
