from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, EventViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'events', EventViewSet)
router.register(r'questions', QuestionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
