from django.db import models
from core.models import AzureStorageBlob, Tag, Language, Editor


class NewsArticle(models.Model):
    foldername = models.CharField(max_length=200, blank=True, default="")
    title = models.CharField(max_length=400)
    subtitle = models.CharField(max_length=400, blank=True, default="")
    summary = models.TextField(blank=True, default="")
    publication_datetime = models.DateTimeField(null=True, blank=True, db_column="PublicationDateTime")
    content_xhtml = models.TextField(blank=True, default="", db_column="ContentXHTML")
    content_markdown = models.TextField(blank=True, default="", db_column="ContentMarkdown")
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="news_articles",
        db_column="LanguageId",
    )
    editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="news_articles",
        db_column="CreatedByEditorId",
    )
    tags_csv = models.TextField(
        blank=True, default="",
        help_text="Legacy CSV tags", db_column="Tags"
    )
    do_not_show = models.BooleanField(default=False, db_column="DoNotShow")
    creation_date = models.DateTimeField(null=True, blank=True, db_column="CreationDate")
    illustration_link = models.CharField(max_length=500, blank=True, default="", db_column="IllustrationLink")
    illustration_label = models.CharField(max_length=300, blank=True, default="", db_column="IllustrationLabel")

    class Meta:
        db_table = "NewsArticles"
        ordering = ["-publication_datetime"]

    def __str__(self):
        return self.title


class NewsArticleImage(models.Model):
    """Additional images attached to a news article."""
    news_article = models.ForeignKey(
        NewsArticle, on_delete=models.CASCADE, related_name="images",
        db_column="NewsArticleId",
    )
    azure_storage_blob = models.ForeignKey(
        AzureStorageBlob, on_delete=models.PROTECT,
        related_name="news_article_images", db_column="AzureStorageBlobId",
    )
    caption = models.CharField(max_length=500, blank=True, default="", db_column="Caption")
    sortorder = models.BigIntegerField(null=True, blank=True, db_column="Sortorder")
    use_as_article_image = models.BooleanField(default=False, db_column="UseAsArticleImage")

    class Meta:
        db_table = "NewsArticleImages"
        ordering = ["sortorder"]

    def __str__(self):
        return str(self.azure_storage_blob)


class NewsArticlesTag(models.Model):
    news_article = models.ForeignKey(
        NewsArticle, on_delete=models.CASCADE, related_name="news_article_tags",
        db_column="NewsArticleId",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="news_article_tags",
        db_column="TagId",
    )

    class Meta:
        db_table = "NewsArticlesTags"
        unique_together = [("news_article", "tag")]

    def __str__(self):
        return f"{self.tag} on {self.news_article}"

