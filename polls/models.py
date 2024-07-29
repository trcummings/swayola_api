from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    vote_count = models.IntegerField(default=0)

    # Limit user to creating only one poll a day
    def can_create_poll(user):
        today = timezone.now().date()
        return not Poll.objects.filter(created_by=user, created_at__date=today).exists()

    def __str__(self):
        return self.title


class Option(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)

    # Each option must be unique per poll. No repeat options
    class Meta:
        unique_together = ('poll', 'text')

    def __str__(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='votes', on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # For now, only one vote per poll
    class Meta:
        unique_together = ('poll', 'voted_by')

    def __str__(self):
        return self.poll + " " + self.option