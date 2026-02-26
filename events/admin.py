from django.contrib import admin
from .models import EventType, Event, EventTag


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ["label"]
    search_fields = ["label"]


class EventTagInline(admin.TabularInline):
    model = EventTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title", "location", "date_from_year", "date_from_month",
        "event_type", "show",
    ]
    list_filter = ["show", "event_type", "language", "date_from_year"]
    search_fields = ["title", "subtitle", "foldername"]
    list_select_related = ["location", "event_type", "language"]
    autocomplete_fields = ["location", "language", "editor"]
    inlines = [EventTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "show"]}),
        ("Dates", {
            "fields": [
                "date_from", "date_from_year", "date_from_month",
                "date_to", "date_to_year", "date_to_month",
            ]
        }),
        ("Location & type", {"fields": ["location", "event_type", "language", "editor"]}),
        ("Content", {"fields": ["description", "content_xhtml", "link",
                                  "illustration_link", "illustration_label"]}),
        ("Metadata", {"fields": ["creation_date"], "classes": ["collapse"]}),
    ]

