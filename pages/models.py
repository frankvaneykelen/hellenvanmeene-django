from django.db import models
from core.models import Tag


class Page(models.Model):
    """
    Self-referential tree: a page can have a parent page.
    Mirrors the ParentId FK in the original schema.
    """
    guid = models.CharField(max_length=36, blank=True, default="")
    foldername = models.CharField(max_length=200, blank=True, default="")
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, blank=True, default="")
    menu_title = models.CharField(max_length=200, blank=True, default="")
    content_xhtml = models.TextField(blank=True, default="")
    content_markdown = models.TextField(blank=True, default="")
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="children",
        db_column="ParentId",
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    sortorder = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Pages"
        ordering = ["sortorder", "title"]

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

