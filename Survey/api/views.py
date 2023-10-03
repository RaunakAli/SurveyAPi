from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SurveySerializer
from .models import Survey
from .models import Survey
from .serializers import SurveySerializer
from rest_framework.response import Response
# Create your views here.
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
#class  SurveryDisplayView():
#class SurveyListView():
