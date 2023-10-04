from rest_framework import routers
from .views import SurveyDetail
from django.urls import path, include



urlpatterns = [
    path('survey/<int:survey_id>/', SurveyDetail.as_view(), name='survey_detail-list'),
]