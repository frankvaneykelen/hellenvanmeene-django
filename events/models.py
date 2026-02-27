from django.db import models
from core.models import Location, Tag, Language, Editor


class EventType(models.Model):
    label = models.CharField(max_length=200)

    class Meta:
        db_table = "EventTypes"
        ordering = ["label"]

    def __str__(self):
        return self.label


class Event(models.Model):
    foldername = models.CharField(max_length=200, blank=True, default="")
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, blank=True, default="")
    description = models.TextField(blank=True, default="")
    link = models.URLField(max_length=500, blank=True, default="")
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
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
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
        db_column="EventTypeId",
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
        db_column="LanguageId",
    )
    editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events",
        db_column="EditorId",
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    creation_date = models.DateTimeField(null=True, blank=True, db_column="CreationDate")

    class Meta:
        db_table = "Events"
        ordering = ["-date_from_year", "-date_from_month"]

    def __str__(self):
        return self.title


class EventTag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_tags",
        db_column="EventId",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="event_tags",
        db_column="TagId",
    )

    class Meta:
        db_table = "EventTags"
        unique_together = [("event", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.event}"

