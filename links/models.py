from django.db import models
from django.utils import timezone
import datetime


class Link(models.Model):
    """
    A Linktree / Link-in-Bio entry. Maps to the Links table.
    """
    label = models.CharField(
        max_length=400,
        help_text="The visible link text / button label.",
    )
    url = models.URLField(max_length=500)
    description = models.TextField(
        blank=True, default="",
        help_text="Optional paragraph of body text shown below the link.",
    )
    boost = models.IntegerField(
        default=0, db_column="SortOrder",
        help_text="Adjusts position relative to natural (newest-first) order. "
                  "Positive = pushed up, negative = pushed down, 0 = default.",
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    updated_at = models.DateTimeField(
        auto_now=True, db_column="UpdatedAt",
        help_text="Automatically set to now whenever the link is saved.",
    )

    class Meta:
        db_table = "Links"
        ordering = ["-id"]
        verbose_name_plural = "links"

    def __str__(self):
        return self.label

    @property
    def is_new(self):
        """True if this link was saved within the last 4 weeks."""
        return self.updated_at >= timezone.now() - datetime.timedelta(weeks=4)
