import json

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SurveyResponse,Survey
from .serializers import SurveyResponseSerializer
from django.shortcuts import get_object_or_404

class SurveyDetail(APIView):
    def get(self, request,survey_id):
        #Takes user_id and survey_id, Returns responses of the user if they exist(AND THE SURVEY),else, just the survey

        user_id = request.user.id

        response_exists = SurveyResponse.objects.filter(survey_id=survey_id, user_id=user_id)

        survey = get_object_or_404(Survey,pk=survey_id)

        response_data = {
            "response":  response_exists[0] if response_exists else None,
            "user_id": user_id,
            "survey": survey.survey,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request,survey_id):
        user_id = 1
        response_data = request.data.get('response', {})
        user_response = SurveyResponse.objects.get_or_create(survey_id=survey_id, user_id=user_id)[0]
        existing_response = user_response.response.update(response_data)
        serializer = SurveyResponseSerializer(user_response,data={},partial=True)
        if serializer.is_valid():
                    serializer.save()
                    #user_response.save()# Save the updated data
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

