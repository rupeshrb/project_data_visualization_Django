from django.db import models

class InternData(models.Model):
    end_year = models.CharField(max_length=255, default='', blank=True)
    intensity = models.IntegerField(null=True, blank=True)
    sector = models.CharField(max_length=255, blank=True)
    topic = models.CharField(max_length=255, blank=True)
    insight = models.TextField()
    url = models.CharField(max_length=512)
    region = models.CharField(max_length=255, blank=True)
    start_year = models.CharField(max_length=255, blank=True)
    impact = models.CharField(max_length=255, blank=True)
    added = models.CharField(max_length=255, blank=True)
    published = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    relevance = models.IntegerField(null=True, blank=True)
    pestle = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    title = models.TextField()
    likelihood = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
