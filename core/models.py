"""
Core app — shared reference models used as FK targets by all other apps.
These correspond to the lookup/reference tables in the original SQL Server schema.
"""

from django.db import models


class Country(models.Model):
    """Maps to: Country table"""
    label = models.CharField(max_length=200, db_column="Name")

    class Meta:
        db_table = "Countries"
        verbose_name_plural = "countries"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Currency(models.Model):
    """ISO currency. Maps to: Currencies table."""
    code   = models.CharField(max_length=3, unique=True)   # EUR, USD, …
    symbol = models.CharField(max_length=4)                # €, $, £, ¥
    name   = models.CharField(max_length=100)              # Euro, US Dollar, …

    class Meta:
        db_table = "Currencies"
        ordering = ["code"]
        verbose_name_plural = "currencies"

    def __str__(self):
        return f"{self.symbol} {self.code}"


class Place(models.Model):
    """City/town. Maps to: Place table."""
    label = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="places", db_column="CountryId")

    class Meta:
        db_table = "Places"
        ordering = ["label"]

    def __str__(self):
        return f"{self.label}, {self.country}"


class Location(models.Model):
    """Museum, gallery, or venue. Maps to: Location table."""
    label = models.CharField(max_length=400)
    place = models.ForeignKey(Place, on_delete=models.PROTECT, related_name="locations", db_column="PlaceId")
    address = models.CharField(max_length=500, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    link = models.URLField(max_length=500, blank=True, default="")

    class Meta:
        db_table = "Locations"
        ordering = ["label"]

    def __str__(self):
        return f"{self.label} ({self.place})"


class Role(models.Model):
    """Curator, artist, author, etc. Maps to: Role table."""
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "Roles"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Creator(models.Model):
    """Person associated with exhibitions or publications. Maps to: Creator table."""
    name = models.CharField(max_length=400)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="creators", db_column="RoleId")
    biography = models.TextField(blank=True, default="")
    photo_link = models.CharField(max_length=500, blank=True, default="", db_column="PhotoLink")
    photo_credit = models.CharField(max_length=300, blank=True, default="", db_column="PhotoCredit")

    class Meta:
        db_table = "Creators"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.role})"


class Language(models.Model):
    """Maps to: Language table."""
    label = models.CharField(max_length=100)

    class Meta:
        db_table = "Languages"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Editor(models.Model):
    """Content editor / staff user label. Maps to: Editor table."""
    label = models.CharField(max_length=200, db_column="Name")

    class Meta:
        db_table = "Editors"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Tag(models.Model):
    """Shared tag used across exhibitions, events, news, pages, publications."""
    label = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = "Tags"
        ordering = ["label"]

    def __str__(self):
        return self.label


class MediaType(models.Model):
    """Maps to: MediaType table."""
    label = models.CharField(max_length=200, db_column="Name")

    class Meta:
        db_table = "MediaTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class CollectionType(models.Model):
    """Maps to: CollectionType table."""
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "CollectionTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class AzureStorageBlob(models.Model):
    """Blob asset registry. Maps to: AzureStorageBlobs table."""
    guid = models.CharField(max_length=36, db_column="Guid")
    container = models.CharField(max_length=250, blank=True, default="", db_column="Container")
    key = models.TextField(blank=True, default="", db_column="Key")
    created = models.DateTimeField(null=True, blank=True, db_column="Created")
    last_modified = models.DateTimeField(null=True, blank=True, db_column="LastModified")
    meta_modified = models.DateTimeField(null=True, blank=True, db_column="MetaModified")
    uri = models.TextField(blank=True, default="", db_column="Uri")
    filename = models.CharField(max_length=500, blank=True, default="", db_column="FileName")
    length = models.BigIntegerField(null=True, blank=True, db_column="Length")
    horizontal_resolution = models.FloatField(null=True, blank=True, db_column="HorizontalResolution")
    vertical_resolution = models.FloatField(null=True, blank=True, db_column="VerticalResolution")
    height = models.BigIntegerField(null=True, blank=True, db_column="Height")
    width = models.BigIntegerField(null=True, blank=True, db_column="Width")
    content_type = models.CharField(max_length=250, blank=True, default="", db_column="ContentType")
    media_type = models.ForeignKey(
        MediaType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="blobs", db_column="MediaTypeId",
    )
    created_by_editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="created_blobs", db_column="CreatedByEditorId",
    )
    last_modified_by_editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="modified_blobs", db_column="LastModifiedByEditorId",
    )

    class Meta:
        db_table = "AzureStorageBlobs"

    def __str__(self):
        return self.filename or self.guid


class Collection(models.Model):
    """Museum/institution collection that holds works. Maps to: Collection table."""
    name = models.CharField(max_length=400)
    place = models.ForeignKey(
        Place, on_delete=models.SET_NULL, null=True, blank=True, related_name="collections",
        db_column="PlaceId",
    )
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="collections",
        db_column="CountryId",
    )
    link = models.URLField(max_length=500, blank=True, default="")
    collection_type = models.ForeignKey(
        CollectionType, on_delete=models.PROTECT, related_name="collections",
        db_column="CollectionTypeId",
    )

    class Meta:
        db_table = "Collections"
        ordering = ["name"]

    def __str__(self):
        return self.name
