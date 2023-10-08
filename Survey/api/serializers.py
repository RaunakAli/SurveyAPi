from rest_framework import serializers
from .models import Survey,SurveyResponse



class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'

    def validate(self, data):
        self.instance
        return data

    def create(self, validated_data):
        # Custom logic for creating SurveyResponse instances
        instance = super(SurveyResponseSerializer, self).create(validated_data)
        self.update_completed(instance)
        return instance

    def update(self, instance, validated_data):
        # Custom logic for updating SurveyResponse instances
        instance = super(SurveyResponseSerializer, self).update(instance, validated_data)
        self.update_completed(instance)
        return instance

    def update_completed(self, instance):
        # Check if all elements in question_name exist in the response
        question_name = instance.survey.questions
        instance.completed = (len(instance.response) == len(question_name)) and all(
            question in instance.response for question in question_name)
