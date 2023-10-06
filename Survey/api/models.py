import json

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
    survey=JSONField(null=False)#Page Elements
    questions=JSONField(null=True)#Questions=name:title
    class Meta:
        managed = False



class SurveyResponse(models.Model):
    survey_id = models.IntegerField()
    user_id = models.IntegerField()
    response_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    response = models.JSONField(default={})


    class Meta:
        managed = False