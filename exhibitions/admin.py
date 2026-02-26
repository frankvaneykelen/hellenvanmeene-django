from django.contrib import admin
from .models import (
    ExhibitionType, Exhibition,
    ExhibitionCreator, ExhibitionMedia, ExhibitionTag, ExhibitionPublication,
)


@admin.register(ExhibitionType)
class ExhibitionTypeAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


class ExhibitionCreatorInline(admin.TabularInline):
    model = ExhibitionCreator
    extra = 1
    autocomplete_fields = ["creator"]


class ExhibitionMediaInline(admin.TabularInline):
    model = ExhibitionMedia
    extra = 1
    autocomplete_fields = ["photo"]
    fields = ["photo", "medium_type", "caption", "sortorder", "indexed"]
    ordering = ["sortorder"]


class ExhibitionTagInline(admin.TabularInline):
    model = ExhibitionTag
    extra = 1
    autocomplete_fields = ["tag"]


class ExhibitionPublicationInline(admin.TabularInline):
    model = ExhibitionPublication
    extra = 1
    autocomplete_fields = ["publication"]


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = [
        "title", "location", "date_from_year", "date_from_month",
        "exhibition_type", "show",
    ]
    list_filter = ["show", "exhibition_type", "language", "date_from_year"]
    search_fields = ["title", "subtitle", "foldername"]
    list_select_related = ["location", "exhibition_type", "language"]
    autocomplete_fields = ["location", "language", "editor"]
    inlines = [
        ExhibitionCreatorInline,
        ExhibitionMediaInline,
        ExhibitionTagInline,
        ExhibitionPublicationInline,
    ]
    fieldsets = [
        (None, {
            "fields": ["title", "subtitle", "foldername", "show"]
        }),
        ("Dates", {
            "fields": [
                "date_from", "date_from_year", "date_from_month",
                "date_to", "date_to_year", "date_to_month",
            ]
        }),
        ("Location & type", {
            "fields": ["location", "exhibition_type", "language", "editor"]
        }),
        ("Content", {
            "fields": ["description", "content_xhtml", "link",
                        "illustration_link", "illustration_label"]
        }),
        ("Metadata", {
            "fields": ["creation_date"],
            "classes": ["collapse"],
        }),
    ]

