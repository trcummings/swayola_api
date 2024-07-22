from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PollViewSet, VoteViewSet, RegisterView, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # User registration / routing
    path('register', RegisterView.as_view(), name='auth_register'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]