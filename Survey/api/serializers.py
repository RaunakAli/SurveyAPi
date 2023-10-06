from rest_framework import serializers
from .models import Survey,SurveyResponse



class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'

    def validate(self, data):
        # Add custom validation logic here
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
        question_name = self.get_question_name(instance)
        instance.completed = (len(instance.response) == len(question_name)) and all(
            question in instance.response for question in question_name)
        instance.save()

    def get_question_name(self, instance):
        survey = instance.survey  # Assuming that you have a foreign key to the Survey model
        return survey.create_questions().keys()



class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    def create_questions(self):
        if self.validated_data.get("survey"):
            data = self.validated_data["survey"]
            question_dict = {}
            for page in data.get("pages", []):
                elements = page.get("elements", [])
                for element in elements:
                    question_name = element.get("name")
                    question_title = element.get("title")
                    if question_name:
                        question_dict[question_name] = question_title
            return question_dict

    @property
    def questions(self):
        return self.create_questions()

    def save(self, *args, **kwargs):
        # Call the parent class's save method to create the Survey instance
        instance = super(SurveySerializer, self).save(*args, **kwargs)

        # Now, you can add the custom logic to create questions and update the instance
        questions = self.create_questions()
        instance.questions = questions
        instance.save()

        return instance