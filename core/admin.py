from django.contrib import admin
from .models import (
    AzureStorageBlob, Collection, CollectionType, Country, Currency,
    Creator, Editor, Language, Location, MediaType, Medium, Place, Role, Tag,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["symbol", "code", "name"]
    search_fields = ["code", "name", "symbol"]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["label", "country"]
    search_fields = ["label"]
    list_filter = ["country"]
    list_select_related = ["country"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["label", "place", "address"]
    search_fields = ["label", "address"]
    list_filter = ["place__country"]
    list_select_related = ["place"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ["name", "role"]
    search_fields = ["name"]
    list_filter = ["role"]
    list_select_related = ["role"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(CollectionType)
class CollectionTypeAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["name", "place", "country", "collection_type"]
    search_fields = ["name"]
    list_filter = ["country", "collection_type"]
    list_select_related = ["place", "country", "collection_type"]


@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    list_display = ["name", "file_name", "extension", "content_type", "width", "height"]
    search_fields = ["name", "file_name", "path", "guid"]
    list_filter = ["extension", "content_type"]
    readonly_fields = [
        "guid", "path", "name", "extension", "file_name", "content_type",
        "content_length", "width", "height", "horizontal_resolution", "vertical_resolution",
        "created_datetime", "last_modified_datetime",
        "media_type", "created_by_editor", "last_modified_by_editor",
    ]


@admin.register(AzureStorageBlob)
class AzureStorageBlobAdmin(admin.ModelAdmin):
    list_display = ["filename", "container", "content_type", "width", "height"]
    search_fields = ["filename", "uri", "key", "guid"]
    list_filter = ["container", "content_type"]
    readonly_fields = [
        "guid", "container", "key", "uri", "filename",
        "length", "width", "height", "horizontal_resolution", "vertical_resolution",
        "content_type", "created", "last_modified", "meta_modified",
        "media_type", "created_by_editor", "last_modified_by_editor",
    ]

