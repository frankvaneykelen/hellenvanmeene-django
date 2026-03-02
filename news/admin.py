from django import forms
from django.contrib import admin
from core.widgets import EasyMDEWidget
from .models import NewsArticle, NewsArticleImage, NewsArticlesTag


class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = "__all__"
        widgets = {
            "content_markdown": EasyMDEWidget,
        }

    def clean_foldername(self):
        foldername = self.cleaned_data.get("foldername", "")
        if foldername:
            qs = NewsArticle.objects.filter(foldername=foldername)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("A news article with this foldername already exists.")
        return foldername


class NewsArticleImageInline(admin.TabularInline):
    model = NewsArticleImage
    extra = 1
    fields = ["azure_storage_blob", "caption", "sortorder", "use_as_article_image"]
    ordering = ["sortorder"]


class NewsArticlesTagInline(admin.TabularInline):
    model = NewsArticlesTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    form = NewsArticleForm
    save_as = True

    class Media:
        js = ("js/admin-slugify.js",)
    list_display = ["title", "publication_datetime", "language", "do_not_show"]
    list_filter = ["do_not_show", "language"]
    search_fields = ["title", "subtitle", "summary", "foldername"]
    list_select_related = ["language", "editor"]
    autocomplete_fields = ["language", "editor"]
    inlines = [NewsArticleImageInline, NewsArticlesTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "do_not_show"]}),
        ("Content", {"fields": ["summary", "content_markdown", "content_xhtml"]}),
        ("Media", {"fields": ["illustration_link", "illustration_label"]}),
        ("Metadata", {"fields": ["publication_datetime", "creation_date",
                                   "language", "editor", "tags_csv"],
                       "classes": ["collapse"]}),
    ]

