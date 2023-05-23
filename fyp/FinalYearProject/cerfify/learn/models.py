from django.db import models
from django.utils import timezone
from django.conf import settings


class Learnm(models.Model):
    Link = models.CharField(max_length=100)
    Description = models.TextField()
    Creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
