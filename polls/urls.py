from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PollListView, PollCreateView, PollDetailView, VoteCreateView, RegisterView, CustomTokenObtainPairView

urlpatterns = [
    # User registration / routing
    path('register', RegisterView.as_view(), name='auth_register'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Polls and votes
    path('polls', PollListView.as_view(), name='poll_list'),
    path('polls/<int:pk>', PollDetailView.as_view(), name='poll_detail'),
    path('polls/create', PollCreateView.as_view(), name='poll_create'),
    path('votes', VoteCreateView.as_view(), name='vote_create'),
]