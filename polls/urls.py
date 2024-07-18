from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]