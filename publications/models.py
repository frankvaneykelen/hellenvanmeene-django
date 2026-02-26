from django.db import models
from core.models import Tag, Place, Creator


class PublicationType(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "PublicationTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class PublicationFormat(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "PublicationFormats"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Publication(models.Model):
    foldername = models.CharField(max_length=200, blank=True, default="")
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, blank=True, default="")
    description = models.TextField(blank=True, default="")
    link = models.URLField(max_length=500, blank=True, default="")
    # publisher is a plain string (no FK) in the original schema
    publisher = models.CharField(max_length=300, blank=True, default="")
    place = models.ForeignKey(
        Place, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="publications",
        help_text="City of publication"
    )
    isbn = models.CharField(max_length=30, blank=True, default="")
    issn = models.CharField(max_length=30, blank=True, default="")
    publication_date = models.DateField(null=True, blank=True)
    date_year = models.IntegerField(null=True, blank=True)
    date_month = models.IntegerField(null=True, blank=True)
    publication_type = models.ForeignKey(
        PublicationType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="publications"
    )
    publication_format = models.ForeignKey(
        PublicationFormat, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="publications"
    )
    show = models.BooleanField(default=True)
    creation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Publications"
        ordering = ["-date_year", "-date_month"]

    def __str__(self):
        return self.title


class PublicationCreator(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="publication_creators"
    )
    creator = models.ForeignKey(
        Creator, on_delete=models.CASCADE, related_name="publication_creators"
    )

    class Meta:
        db_table = "PublicationCreators"
        unique_together = [("publication", "creator")]

    def __str__(self):
        return f"{self.creator} in {self.publication}"


class PublicationTag(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, related_name="publication_tags"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="publication_tags")

    class Meta:
        db_table = "PublicationTags"
        unique_together = [("publication", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.publication}"

