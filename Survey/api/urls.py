from rest_framework import routers
from .views import SurveyDetail,Survey_Response
from django.urls import path, include



urlpatterns = [
    path('survey/<int:survey_id>/', SurveyDetail.as_view(), name='survey_detail-list'),
    path('survey/submit/<int:survey_id>/', SurveyDetail.as_view(), name='survey_detail-submit'),
    path('survey_response/<int:survey_id>/', Survey_Response.as_view(), name='survey-response-get'),
    path('survey_response', Survey_Response.as_view(), name='survey-response-post'),
]