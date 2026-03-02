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
        related_name="exhibitions",
        db_column="LocationId",
    )
    date_from = models.DateField(null=True, blank=True, db_column="DateFrom")
    date_from_year = models.IntegerField(null=True, blank=True, db_column="DateFromYear")
    date_from_month = models.IntegerField(null=True, blank=True, db_column="DateFromMonth")
    date_to = models.DateField(null=True, blank=True, db_column="DateTo")
    date_to_year = models.IntegerField(null=True, blank=True, db_column="DateToYear")
    date_to_month = models.IntegerField(null=True, blank=True, db_column="DateToMonth")

    content_xhtml = models.TextField(blank=True, default="", db_column="ContentXHTML")
    illustration_link = models.CharField(max_length=500, blank=True, default="", db_column="IllustrationLink")
    illustration_label = models.CharField(max_length=300, blank=True, default="", db_column="IllustrationLabel")
    exhibition_type = models.ForeignKey(
        ExhibitionType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions",
        db_column="ExhibitionTypeId",
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions",
        db_column="LanguageId",
    )
    editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="exhibitions",
        db_column="EditorId",
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    creation_date = models.DateTimeField(null=True, blank=True, db_column="CreationDate")

    class Meta:
        db_table = "Exhibitions"
        ordering = ["-date_from_year", "-date_from_month"]

    def __str__(self):
        return self.title


class ExhibitionCreator(models.Model):
    """M2M through-table: Exhibition <-> Creator."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_creators",
        db_column="ExhibitionId",
    )
    creator = models.ForeignKey(
        Creator, on_delete=models.CASCADE, related_name="exhibition_creators",
        db_column="CreatorId",
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
        related_name="exhibition_media",
        db_column="ExhibitionId",
    )
    photo = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="exhibition_media",
        null=True, blank=True, db_column="MediumId"
    )
    medium_type = models.CharField(max_length=100, blank=True, default="", db_column="MediumType")
    caption = models.CharField(max_length=500, blank=True, default="", db_column="Caption")
    indexed = models.BooleanField(null=True, blank=True, db_column="Indexed")
    sortorder = models.BigIntegerField(null=True, blank=True, db_column="Sortorder")

    class Meta:
        db_table = "ExhibitionMedia"
        ordering = ["sortorder"]

    def __str__(self):
        return f"{self.photo} in {self.exhibition} (#{self.sortorder})"


class ExhibitionTag(models.Model):
    """M2M through-table: Exhibition <-> Tag."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_tags",
        db_column="ExhibitionId",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="exhibition_tags",
        db_column="TagId",
    )

    class Meta:
        db_table = "ExhibitionTags"
        unique_together = [("exhibition", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.exhibition}"


class ExhibitionPublication(models.Model):
    """M2M through-table: Exhibition <-> Publication."""
    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name="exhibition_publications",
        db_column="ExhibitionId",
    )
    # String reference to avoid circular import with publications app
    publication = models.ForeignKey(
        "publications.Publication",
        on_delete=models.CASCADE, related_name="exhibition_publications",
        db_column="PublicationId",
    )

    class Meta:
        db_table = "ExhibitionPublications"
        unique_together = [("exhibition", "publication")]

    def __str__(self):
        return f"{self.publication} in {self.exhibition}"

