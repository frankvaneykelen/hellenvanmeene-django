from django.db import models
from core.models import Tag


class Page(models.Model):
    """
    Self-referential tree: a page can have a parent page.
    Mirrors the ParentId FK in the original schema.
    """
    guid = models.CharField(max_length=36, blank=True, default="", db_column="Guid")
    foldername = models.CharField(max_length=200, blank=True, default="", db_column="Foldername")
    title = models.CharField(max_length=400, db_column="Title")
    subtitle = models.CharField(max_length=400, blank=True, default="", db_column="Subtitle")
    menu_title = models.CharField(max_length=200, blank=True, default="", db_column="MenuTitle")
    content_xhtml = models.TextField(blank=True, default="", db_column="ContentXHTML")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="children",
        db_column="ParentId",
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    creation_date = models.DateTimeField(null=True, blank=True, db_column="CreationDate")

    class Meta:
        db_table = "Pages"
        ordering = ["title"]

    def __str__(self):
        return self.title


class PageTag(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="page_tags",
        db_column="PageId",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="page_tags",
        db_column="TagId",
    )

    class Meta:
        db_table = "PageTags"
        unique_together = [("page", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.page}"

