from rest_framework import routers
from .views import SurveyViewSet

router = routers.DefaultRouter()
router.register(r'surveys', SurveyViewSet)


urlpatterns = router.urls