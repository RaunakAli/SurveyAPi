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


class SurveyResponse(models.Model):
    survey_id = models.IntegerField()
    user_id = models.IntegerField()
    response_timestamp = models.DateTimeField()
    completed = models.BooleanField(default=False)

    question_name = models.JSONField()
    response = models.JSONField()

    def save(self, *args, **kwargs):
        # Check if all elements in question_name exist in the response
        self.completed = (len(self.response) == len(self.question_name)) and all(question in self.response for question in self.question_name)
        super(SurveyResponse, self).save(*args, **kwargs)