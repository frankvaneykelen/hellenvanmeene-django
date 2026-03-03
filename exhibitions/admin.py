from django import forms
from django.contrib import admin
from core.widgets import EasyMDEWidget
from .models import (
    ExhibitionType, Exhibition,
    ExhibitionCreator, ExhibitionMedia, ExhibitionTag, ExhibitionPublication,
)


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = "__all__"
        widgets = {
            "description": EasyMDEWidget,
        }

    def clean_foldername(self):
        foldername = self.cleaned_data.get("foldername", "")
        if foldername:
            qs = Exhibition.objects.filter(foldername=foldername)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("An exhibition with this foldername already exists.")
        return foldername


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
    autocomplete_fields = ["medium"]
    fields = ["medium", "medium_type", "caption", "sortorder", "indexed"]
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
    form = ExhibitionForm
    save_as = True

    class Media:
        js = ("js/admin-slugify.js",)
    list_display = [
        "title", "location", "date_from_year", "date_from_month",
        "exhibition_type", "do_not_show",
    ]
    list_filter = ["do_not_show", "exhibition_type", "language", "date_from_year"]
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
            "fields": ["title", "subtitle", "foldername", "do_not_show"]
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

