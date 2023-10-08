from rest_framework import routers
from .views import SurveyDetail, SurveyList, SurveyDetailUpdateView
from django.urls import path, include



urlpatterns = [
    path('survey/<int:id>/', SurveyDetail.as_view(), name='survey_detail-list'),
    path('survey/<int:survey_id>/submit/', SurveyDetailUpdateView.as_view(), name='submit-response'),
    path('survey/', SurveyList.as_view(), name='survey-list'),
]