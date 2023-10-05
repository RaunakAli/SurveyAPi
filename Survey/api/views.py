import json

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SurveyResponse,Survey
from .serializers import SurveyResponseSerializer,SurveySerializer

class SurveyDetail(APIView):
    def get(self, request,survey_id):
        #Takes user_id and survey_id, Returns responses of the user if they exist(AND THE SURVEY),else, just the survey

        user_id = request.user.id
        try:
            response = SurveyResponse.objects.get(survey_id=survey_id, user_id=user_id)
            response_serializer = SurveyResponseSerializer(response)
            survey = Survey.objects.get(id=survey_id)
            survey_serializer = SurveySerializer(survey)

            return Response({
                "response": response_serializer.data,
                "user_id": user_id,
                "survey": survey_serializer.data,
            }, status=status.HTTP_200_OK)

        except SurveyResponse.DoesNotExist:
            # If no response exists, return only survey details
            survey = Survey.objects.get(id=survey_id)
            survey_serializer = SurveySerializer(survey)
            return Response({
                "response": "USER's FirstAttempt",
                "user_id": user_id,
                "survey": survey_serializer.data,
            }, status=status.HTTP_200_OK)
            # return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request,survey_id):
        user_id = request.user.id
        response_data = request.data.get('response', {})
        user_response = SurveyResponse.objects.get_or_create(survey_id=survey_id, user_id=user_id)
        #existing_response = user_response.response
        updated_data = {
                    "response":  user_response.response.update(response_data)
                }
        serializer = SurveyResponseSerializer(user_response, data=updated_data,partial=True)
        if serializer.is_valid():
                    serializer.save()
                    #user_response.save()# Save the updated data
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class Survey_Response(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id):
        user_id = request.user.id
        try:
            response = SurveyResponse.objects.get(survey_id=survey_id, user_id=user_id)
            response_serializer = SurveyResponseSerializer(response)
            survey = Survey.objects.get(id=survey_id)
            survey_serializer = SurveySerializer(survey)
            return Response({"response": response_serializer.data,
                "user_id": user_id,
                "survey": survey_serializer.data,},status=status.HTTP_200_OK)
        except SurveyResponse.DoesNotExist:
            # If no response exists, return only survey details
            survey = Survey.objects.get(id=survey_id)
            survey_serializer = SurveySerializer(survey)
            return Response({"response": "User's First Attempt",
                "user_id": user_id,
                "survey": survey_serializer.data,}, status=status.HTTP_200_OK)
            #return Response({"message": "Survey not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_id = request.user.id
        survey_id = request.data.get('survey_id')
        try:
            response = SurveyResponse.objects.get(survey_id=survey_id, user_id=user_id)
            # If a response already exists, you can update it here
            serializer = SurveyResponseSerializer(response, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SurveyResponse.DoesNotExist:
            # If no response exists, you can create a new one here
            serializer = SurveyResponseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=user_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

