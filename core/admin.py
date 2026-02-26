from django.contrib import admin
from .models import (
    Country, Place, Location, Role, Creator,
    Language, Editor, Tag, MediaType, CollectionType, Collection,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


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

