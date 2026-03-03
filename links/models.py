from django.db import models


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
    sortorder = models.IntegerField(default=0, db_column="SortOrder")
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")

    class Meta:
        db_table = "Links"
        ordering = ["sortorder", "id"]
        verbose_name_plural = "links"

    def __str__(self):
        return self.label
