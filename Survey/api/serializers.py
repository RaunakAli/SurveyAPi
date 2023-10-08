from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Survey,SurveyResponse

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    def validate(self, data):
        if  data.get('start_date') >= data.get('end_date'):
            raise serializers.ValidationError("Start date must be before the end date.")
        return data

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'

    def validate(self, data):
        instance = self.instance
        if len(instance.survey.questions.keys()) < len(instance.response):
            raise serializers.ValidationError("No of responses are more than No of Questions")
        instance.is_completed = all(question in instance.response for question in instance.survey.questions.keys())
        return data
