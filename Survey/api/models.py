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
    survey=JSONField(null=False)
    questions=JSONField(null=True)
    @property
    def create_questions(self):
        if self.survey:
                data = self.survey
                question_dict = {}
                for page in data.get("pages", []):
                    elements = page.get("elements", [])
                    for element in elements:
                        question_name = element.get("name")
                        question_title = element.get("title")
                        if question_name:
                            question_dict[question_name] = question_title
                return question_dict



class SurveyResponse(models.Model):
    survey_id = models.IntegerField()
    user_id = models.IntegerField()
    response_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    question_name = models.JSONField()
    response = models.JSONField(default={})

    def save(self, *args, **kwargs):
        # Check if all elements in question_name exist in the response
        self.completed = (len(self.response) == len(self.question_name)) and all(question in self.response for question in self.question_name)
        super(SurveyResponse, self).save(*args, **kwargs)