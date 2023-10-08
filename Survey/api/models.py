import json

from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.contrib.auth.models import User


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    is_live = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    discription = models.TextField()
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    survey = JSONField(null=False)  # Page Elements
    questions = JSONField(null=True,blank=True)  # Questions=name:title

    class Meta:
        managed = False
        db_table = "survey_db_palladium"

    def genrate_questions(self):
        data = self.survey
        self.questions = {
            element["name"]: element["title"]
            for page in data.get("pages", [])
            for element in page.get("elements", [])
            if element.get("name") and element.get("title")
        }

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.genrate_questions()
        super(Survey, self).save(force_insert,force_update,using,update_fields)


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_timestamp = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    response = models.JSONField(default=dict())

    class Meta:
        managed = False
        db_table = "surveyresponse_db_palladium"
