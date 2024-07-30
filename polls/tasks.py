from celery import shared_task
from django.core.cache import cache
from .models import Poll

# Task to increment the cached denormalized vote count on every poll option
@shared_task
def increment_vote_count(poll_id, option_id):
    poll_key = f'poll_{poll_id}_vote_count'
    option_key = f'option_{option_id}_vote_count'
    
    cache.incr(poll_key)
    cache.incr(option_key)

# Task to update the vote counts in the database
@shared_task
def write_vote_counts_to_db():
    # Grab all polls with options prefetched
    polls = Poll.objects.prefetch_related('options').all()

    # Itereate over each poll and update the vote count and option vote counts
    for poll in polls:
        poll_key = f'poll_{poll.id}_vote_count'
        # Pull cached count and update
        vote_count = cache.get(poll_key)

        # If there's nothing in the cache, ignore
        if vote_count is not None:
            poll.vote_count = vote_count
            poll.save()

        # Create var to track running total
        total_option_votes = 0

        # For each option in the poll, update the vote count with the cached value
        for option in poll.options.all():
            option_key = f'option_{option.id}_vote_count'
            option_vote_count = cache.get(option_key)

            # If there's nothing in the cache, ignore
            if option_vote_count is not None:
                option.vote_count = option_vote_count
                option.save()
            
            # Increment the running total with the individual option amount
            total_option_votes += option.vote_count

        # Ensure poll vote counts are the sum of their options' vote counts,
        # the options take priority, the totals should always add up.
        if poll.vote_count != total_option_votes:
            poll.vote_count = total_option_votes
            poll.save()