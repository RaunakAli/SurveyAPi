from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SurveyResponse,Survey
from .serializers import SurveyResponseSerializer,SurveySerializer

class SurveyDetail(APIView):
    def get(self, request,survey_id):

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
        try:
            user_response = SurveyResponse.objects.get(survey_id=survey_id, user_id=user_id)
            if user_response and not  user_response.completed :
                existing_response = user_response.response
                existing_response.update(response_data)
                user_response.response = existing_response
                updated_data = {
                    "user_id": user_id,
                    "survey_id": survey_id,
                    "question_name": user_response.question_name,
                    "response": existing_response,
                }
                serializer = SurveyResponseSerializer(user_response, data=updated_data)
                if serializer.is_valid():
                    serializer.save()
                    user_response.save()# Save the updated data
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("ALREADY FILLED BY THE USER", status=status.HTTP_200_OK)
        except SurveyResponse.DoesNotExist:
            survey = Survey.objects.get(id=survey_id)
            survey_serializer = SurveySerializer(survey)
            questions_data = survey_serializer.data.get('questions')
            question_name_to_title = {
                question["name"]: question["title"]
                for question in questions_data
            }
            response_data = request.data.get('response', {})
            serializer_data = {
                "user_id": user_id,
                "survey_id": survey_id,
                "question_name": question_name_to_title,
                "response": response_data,
            }
            serializer = SurveyResponseSerializer(data=serializer_data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data["response"] = response_data  # Update the validated data
                serializer.save(**validated_data)  # Pass the validated data as keyword arguments
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("ISSUES?", status=status.HTTP_400_BAD_REQUEST)



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

