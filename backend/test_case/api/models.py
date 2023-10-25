from django.db import models


class Bookmark(models.Model):
    url = models.URLField(verbose_name="URL", unique=True)
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    description = models.TextField(verbose_name="Description", blank=True)
    favicon = models.URLField(verbose_name="Favicon URL", blank=True)
