from django.contrib import admin
from .models import (
    PublicationType, PublicationFormat, Publication,
    PublicationCreator, PublicationTag,
)


@admin.register(PublicationType)
class PublicationTypeAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(PublicationFormat)
class PublicationFormatAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


class PublicationCreatorInline(admin.TabularInline):
    model = PublicationCreator
    extra = 1
    autocomplete_fields = ["creator"]


class PublicationTagInline(admin.TabularInline):
    model = PublicationTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "title", "publisher", "place", "date_year",
        "publication_type", "show",
    ]
    list_filter = ["show", "publication_type", "publication_format", "date_year"]
    search_fields = ["title", "subtitle", "publisher", "isbn", "issn", "foldername"]
    list_select_related = ["place", "publication_type"]
    autocomplete_fields = ["place"]
    inlines = [PublicationCreatorInline, PublicationTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "show"]}),
        ("Publisher", {"fields": ["publisher", "place", "publication_type", "publication_format"]}),
        ("Identifiers", {"fields": ["isbn", "issn", "link"]}),
        ("Date", {"fields": ["publication_date", "date_year", "date_month"]}),
        ("Content", {"fields": ["description"]}),
        ("Metadata", {"fields": ["creation_date"], "classes": ["collapse"]}),
    ]

