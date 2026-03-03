"""
Gallery model — art galleries that represent Hellen van Meene.

Uses core.Place (→ core.Country) for location.
"""

from django.db import models
from core.models import Place


class Gallery(models.Model):
    slug = models.SlugField(
        max_length=200, unique=True,
        help_text="URL-friendly identifier, e.g. 'galerie-fontana'",
    )
    name = models.CharField(max_length=400)
    place = models.ForeignKey(
        Place, on_delete=models.PROTECT, related_name="galleries",
        db_column="PlaceId",
    )
    description = models.TextField(
        blank=True, default="",
        help_text="Supports Markdown.",
    )
    website = models.URLField(max_length=500, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    phone2 = models.CharField(max_length=50, blank=True, default="", db_column="Phone2")
    image_link = models.CharField(
        max_length=500, blank=True, default="", db_column="ImageLink",
        help_text="Cloud image path, e.g. /cloud/website-images/galerie-fontana.jpg",
    )
    image_alt = models.CharField(max_length=400, blank=True, default="", db_column="ImageAlt")
    sortorder = models.IntegerField(default=0, db_column="SortOrder")
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")

    class Meta:
        db_table = "Galleries"
        ordering = ["sortorder", "name"]
        verbose_name_plural = "galleries"

    def __str__(self):
        return f"{self.name} ({self.place})"
