from django import forms
from django.contrib import admin
from core.widgets import EasyMDEWidget
from .models import EventType, Event, EventTag


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "description": EasyMDEWidget,
        }

    def clean_foldername(self):
        foldername = self.cleaned_data.get("foldername", "")
        if foldername:
            qs = Event.objects.filter(foldername=foldername)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An event with this foldername already exists.")
        return foldername


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
    form = EventForm
    save_as = True

    class Media:
        js = ("js/admin-slugify.js",)
    list_display = [
        "title", "location", "date_from_year", "date_from_month",
        "event_type", "do_not_show",
    ]
    list_filter = ["do_not_show", "event_type", "language", "date_from_year"]
    search_fields = ["title", "subtitle", "foldername"]
    list_select_related = ["location", "event_type", "language"]
    autocomplete_fields = ["location", "language", "editor"]
    inlines = [EventTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "do_not_show"]}),
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

