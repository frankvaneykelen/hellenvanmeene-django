from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ["code", "year", "public", "show", "greatest_hits"]
    list_filter = ["public", "show", "greatest_hits", "year"]
    search_fields = ["code", "tags_csv", "notes_markdown"]
    list_editable = ["public", "show", "greatest_hits"]
    readonly_fields = ["tag_list_display"]

    @admin.display(description="Tags")
    def tag_list_display(self, obj):
        return ", ".join(obj.tag_list)

