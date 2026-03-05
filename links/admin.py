from django.contrib import admin
from .models import Link


@admin.action(description="Duplicate selected links")
def duplicate_links(modeladmin, request, queryset):
    for link in queryset:
        link.pk = None
        link.label = f"{link.label} (copy)"
        link.save()


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ["boost", "label", "url", "do_not_show"]
    list_editable = ["boost", "do_not_show"]
    list_display_links = ["label"]
    search_fields = ["label", "url", "description"]
    ordering = ["-id"]
    actions = [duplicate_links]
    save_as = True
