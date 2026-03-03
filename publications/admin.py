from django import forms
from django.contrib import admin
from core.widgets import EasyMDEWidget
from .models import (
    PublicationType, PublicationFormat, Publication,
    PublicationCreator, PublicationTag, PublicationMedia,
)


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = "__all__"
        widgets = {
            "description": EasyMDEWidget,
        }

    def clean_foldername(self):
        foldername = self.cleaned_data.get("foldername", "")
        if foldername:
            qs = Publication.objects.filter(foldername=foldername)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A publication with this foldername already exists.")
        return foldername


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


class PublicationMediaInline(admin.TabularInline):
    model = PublicationMedia
    extra = 1
    autocomplete_fields = ["medium"]
    fields = ["medium", "medium_type", "caption", "sortorder", "indexed"]
    ordering = ["sortorder"]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    form = PublicationForm
    save_as = True

    class Media:
        js = ("js/admin-slugify.js",)
    list_display = [
        "title", "publisher", "place", "date_year",
        "publication_type", "do_not_show",
    ]
    list_filter = ["do_not_show", "publication_type", "publication_format", "date_year"]
    search_fields = ["title", "subtitle", "publisher", "isbn", "issn", "foldername"]
    list_select_related = ["place", "publication_type"]
    autocomplete_fields = ["place"]
    inlines = [PublicationCreatorInline, PublicationTagInline, PublicationMediaInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "do_not_show"]}),
        ("Publisher", {"fields": ["publisher", "place", "publication_type", "publication_format"]}),
        ("Identifiers", {"fields": ["isbn", "issn", "link"]}),
        ("Date", {"fields": ["publication_date", "date_year", "date_month"]}),
        ("Content", {"fields": ["description"]}),
        ("Metadata", {"fields": ["creation_date"], "classes": ["collapse"]}),
    ]

