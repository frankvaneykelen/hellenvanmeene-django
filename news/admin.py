from django.contrib import admin
from .models import NewsArticle, NewsArticleImage, NewsArticlesTag


class NewsArticleImageInline(admin.TabularInline):
    model = NewsArticleImage
    extra = 1
    fields = ["image_link", "caption", "sortorder"]
    ordering = ["sortorder"]


class NewsArticlesTagInline(admin.TabularInline):
    model = NewsArticlesTag
    extra = 1
    autocomplete_fields = ["tag"]


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "publication_datetime", "language", "show"]
    list_filter = ["show", "language"]
    search_fields = ["title", "subtitle", "summary", "foldername"]
    list_select_related = ["language", "editor"]
    autocomplete_fields = ["language", "editor"]
    inlines = [NewsArticleImageInline, NewsArticlesTagInline]
    fieldsets = [
        (None, {"fields": ["title", "subtitle", "foldername", "show"]}),
        ("Content", {"fields": ["summary", "content_markdown", "content_xhtml"]}),
        ("Media", {"fields": ["illustration_link", "illustration_label"]}),
        ("Metadata", {"fields": ["publication_datetime", "creation_date",
                                   "language", "editor", "tags_csv"],
                       "classes": ["collapse"]}),
    ]

