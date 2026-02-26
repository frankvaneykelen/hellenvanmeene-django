"""
Exhibition models.

Exhibition
  +-- Location (via core.Location)
  +-- ExhibitionCreator  -> Creator
  +-- ExhibitionMedia    -> Photo
  +-- ExhibitionTag      -> Tag
  +-- ExhibitionPublication -> Publication
"""

from django.db import models
from core.models import Location, Creator, Tag, Language, Editor
from photos.models import Photo


class ExhibitionType(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "ExhibitionTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Exhibition(models.Model):
    foldername = models.CharField(max_length=200, blank=True, default="")
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, blank=True, default="")
    description = models.TextField(blank=True, default="")
    link = models.URLField(max_length=500, blank=True, default="")

    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions"
    )
    date_from = models.DateField(null=True, blank=True)
    date_from_year = models.IntegerField(null=True, blank=True)
    date_from_month = models.IntegerField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    date_to_year = models.IntegerField(null=True, blank=True)
    date_to_month = models.IntegerField(null=True, blank=True)

    content_xhtml = models.TextField(blank=True, default="")
    illustration_link = models.CharField(max_length=500, blank=True, default="")
    illustration_label = models.CharField(max_length=300, blank=True, default="")
    exhibition_type = models.ForeignKey(
        ExhibitionType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions"
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions"
    )
    editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions"
    )
    show = models.BooleanField(default=True)
    creation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Exhibitions"
        ordering = ["-date_from_year", "-date_from_month"]

    def __str__(self):
        return self.title


class ExhibitionCreator(models.Model):
    """M2M through-table: Exhibition <-> Creator."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_creators"
    )
    creator = models.ForeignKey(
        Creator, on_delete=models.CASCADE, related_name="exhibition_creators"
    )

    class Meta:
        db_table = "ExhibitionCreators"
        unique_together = [("exhibition", "creator")]

    def __str__(self):
        return f"{self.creator} @ {self.exhibition}"


class ExhibitionMedia(models.Model):
    """Links a Photo to an Exhibition with optional caption and sort order."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, null=True, blank=True,
        related_name="exhibition_media"
    )
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="exhibition_media",
        null=True, blank=True, db_column="MediumId"
    )
    medium_type = models.CharField(max_length=100, blank=True, default="")
    caption = models.CharField(max_length=500, blank=True, default="")
    indexed = models.BooleanField(null=True, blank=True)
    sortorder = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = "ExhibitionMedia"
        ordering = ["sortorder"]

    def __str__(self):
        return f"{self.photo} in {self.exhibition} (#{self.sortorder})"


class ExhibitionTag(models.Model):
    """M2M through-table: Exhibition <-> Tag."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_tags"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="exhibition_tags")

    class Meta:
        db_table = "ExhibitionTags"
        unique_together = [("exhibition", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.exhibition}"


class ExhibitionPublication(models.Model):
    """M2M through-table: Exhibition <-> Publication."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_publications"
    )
    # String reference to avoid circular import with publications app
    publication = models.ForeignKey(
        "publications.Publication",
        on_delete=models.CASCADE, related_name="exhibition_publications"
    )

    class Meta:
        db_table = "ExhibitionPublications"
        unique_together = [("exhibition", "publication")]

    def __str__(self):
        return f"{self.publication} in {self.exhibition}"

