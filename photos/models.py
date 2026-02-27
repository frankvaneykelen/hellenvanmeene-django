"""Photo model. Maps to: Photos table in the original SQL Server schema."""

from django.db import models


class Photo(models.Model):
    """
    Core asset of the site. Each photo is stored in Azure Blob Storage;
    cloud_link holds the blob path/URL.
    """
    code = models.CharField(max_length=100, unique=True, help_text="Archive code, e.g. HvM-001", db_column="Code")
    year = models.SmallIntegerField(null=True, blank=True, db_column="Year")
    cloud_link = models.CharField(
        max_length=500, blank=True, default="",
        help_text="Azure Blob Storage path relative to container root",
        db_column="CloudLink",
    )
    public = models.BooleanField(default=True, db_column="Public")
    show = models.BooleanField(default=True, db_column="Show")
    greatest_hits = models.BooleanField(default=False, db_column="GreatestHits")
    tags_csv = models.TextField(
        blank=True, default="",
        help_text="Legacy comma-separated tags from the original CMS",
        db_column="Tags"
    )
    added_datetime = models.DateTimeField(null=True, blank=True, db_column="AddedDatetime")
    notes_markdown = models.TextField(blank=True, default="", db_column="NotesMarkdown")

    class Meta:
        db_table = "Photos"
        ordering = ["-code"]

    def __str__(self):
        return self.code

    @property
    def tag_list(self):
        """Return tags_csv as a cleaned Python list."""
        return [t.strip() for t in self.tags_csv.split(",") if t.strip()]

