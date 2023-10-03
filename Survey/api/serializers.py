from rest_framework import serializers
from .models import Survey

class TextFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    rows = serializers.IntegerField()
    autogrow = serializers.BooleanField()
    maxLength = serializers.IntegerField()
    isRequired = serializers.BooleanField()
    requiredErrorText = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()


class RatingFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    title = serializers.CharField()
    isRequired = serializers.BooleanField()
    rateCount = serializers.IntegerField()
    rateMin = serializers.IntegerField()
    rateMax = serializers.IntegerField()
    minRateDescription = serializers.CharField()
    maxRateDescription = serializers.CharField()

class CheckboxFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    visibleIf = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    isRequired = serializers.BooleanField()
    validators = serializers.ListField(child=serializers.DictField())
    choices = serializers.ListField()
    showOtherItem = serializers.BooleanField()
    otherText = serializers.CharField()
    colCount = serializers.IntegerField()

class CommentFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    visibleIf = serializers.CharField()
    title = serializers.CharField()
    isRequired = serializers.BooleanField()

class BooleanFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    title = serializers.CharField()
    isRequired = serializers.BooleanField()

class DropdownFieldSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    title = serializers.CharField()
    isRequired = serializers.BooleanField()
    choices = serializers.ListField(child=serializers.DictField())







class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    def get_questions(self, instance):
        questions = instance.questions
        serialized_questions = []

        for question in questions:
            question_type = question.get('type', 'text')
            if question_type == 'CommentField':
                serializer = CommentFieldSerializer(data=question)
            elif question_type == 'TextField':
                serializer = TextFieldSerializer(data=question)
            elif question_type =='RatingField':
                serializer = RatingFieldSerializer(data=question)
            elif question_type == 'CheckboxField':
                serializer = CheckboxFieldSerializer(data=question)
            elif question_type =='BooleanField':
                serializer = BooleanFieldSerializer(data=question)
            else:
                serializer = DropdownFieldSerializer(data=question)

            if serializer.is_valid():
                serialized_questions.append(serializer.validated_data)
            else:
                serialized_questions.append({'error': 'Invalid question data'})

        return serialized_questions