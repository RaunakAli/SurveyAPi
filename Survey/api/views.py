import json
from rest_framework import generics

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SurveyResponse,Survey
from .serializers import SurveyResponseSerializer, SurveySerializer
from django.shortcuts import get_object_or_404

class SurveyDetail(generics.RetrieveUpdateAPIView):
    #Retrieves the Survey(Detail) and response(If exists), And can be used to update the Survey(post)
    # Will be used to  do EXPORTCSV with post
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):

        user_id = self.request.user.id
        survey = self.get_object()
        user_response = SurveyResponse.objects.filter(survey_id=survey.id, user_id=user_id).first()
        response_data = {
            "response": SurveyResponseSerializer(user_response).data["response"] if user_response else None,
            "user_id": user_id,
            "survey": survey.survey,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class SurveyDetailUpdateView(generics.UpdateAPIView):
    #If response found updates the "response" Field else creates a new Response

    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    lookup_url_kwarg = 'survey_id'  # Assuming 'survey_id' is the URL parameter you use for lookup

    def get_object(self):
        user_id = self.request.user.id # Replace with the actual user_id as needed
        survey_id = self.kwargs.get('survey_id')
        obj, created = SurveyResponse.objects.get_or_create(survey_id=survey_id, user_id=user_id)
        return obj
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = request.data.get('response', {})
        # Update the response_data by merging it with the existing data
        instance.response.update(response_data)
        serializer = self.get_serializer(instance, partial=True,data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)#TOOD:- Let it oonly return a Ok message
class SurveyList(generics.ListCreateAPIView):
    # A get request Lists all the survey, A post request allows us to make a new  survey
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def perform_create(self, serializer):
        serializer.save()  # This will save the new Survey object

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)