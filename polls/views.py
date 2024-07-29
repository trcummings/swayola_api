from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer, RegisterSerializer, CustomTokenObtainPairSerializer

# region Polls
class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollCreateView(generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Make sure users can only create one poll per day
    def perform_create(self, serializer):
        if not Poll.can_create_poll(self.request.user):
            raise PermissionDenied("You can only create one poll per day.")
        serializer.save(created_by=self.request.user)

class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
# endregion

# region Votes
class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure we can't vote on a poll that we created
    def perform_create(self, serializer):
        poll = serializer.validated_data['poll']
        if poll.created_by == self.request.user:
            raise PermissionDenied("You cannot vote on your own poll.")
        serializer.save(voted_by=self.request.user)
# endregion

# region Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    # Pull the IP address out of the request meta if possible
    def perform_create(self, serializer):
        ip_address = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip_address)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# endregion