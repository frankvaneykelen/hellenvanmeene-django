from django import forms
from django.contrib import admin
from .models import Page, PageTag


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"

    def clean_foldername(self):
        foldername = self.cleaned_data.get("foldername", "")
        if foldername:
            qs = Page.objects.filter(foldername=foldername)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A page with this foldername already exists.")
        return foldername


class PageTagInline(admin.TabularInline):
    model = PageTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    save_as = True

    class Media:
        js = ("js/admin-slugify.js",)
    list_display = ["title", "parent", "menu_title", "foldername", "do_not_show"]
    list_filter = ["do_not_show"]
    search_fields = ["title", "subtitle", "menu_title", "foldername", "guid"]
    list_editable = ["do_not_show"]
    autocomplete_fields = ["parent"]
    inlines = [PageTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "menu_title", "foldername",
                            "guid", "parent", "do_not_show"]}),
        ("Content", {"fields": ["content_xhtml"]}),
        ("Metadata", {"fields": ["creation_date"], "classes": ["collapse"]}),
    ]

