from django.db import models
from django.db.models import JSONField
from django.utils import timezone



class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    is_live = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    questions=JSONField(null=True)