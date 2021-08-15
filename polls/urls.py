from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PollViewSet, QuestionViewSet

router = DefaultRouter()

router.register("polls", PollViewSet, basename="polls")
router.register(
    r"polls/(?P<poll_pk>\d+)/questions", QuestionViewSet, basename="questions"
)


urlpatterns = [
    path("v1/", include(router.urls)),
]
