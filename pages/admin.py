from django.contrib import admin
from .models import Page, PageTag


class PageTagInline(admin.TabularInline):
    model = PageTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "parent", "menu_title", "foldername", "show", "sortorder"]
    list_filter = ["show"]
    search_fields = ["title", "subtitle", "menu_title", "foldername", "guid"]
    list_editable = ["show", "sortorder"]
    autocomplete_fields = ["parent"]
    inlines = [PageTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "menu_title", "foldername",
                            "guid", "parent", "show", "sortorder"]}),
        ("Content", {"fields": ["content_markdown", "content_xhtml"]}),
        ("Metadata", {"fields": ["creation_date"], "classes": ["collapse"]}),
    ]

