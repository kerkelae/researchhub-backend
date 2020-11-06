from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from django.utils import timezone

from user.models import User
from discussion.models import Thread, Comment, Reply
import uuid

class Command(BaseCommand):

    def handle(self, *args, **options):
        three_days_ago = timezone.now().date() - timedelta(days=3)
        objects = User.objects.filter(created_date__lte=three_days_ago, probable_spammer=True)
        count = objects.count()
        for i, user in enumerate(objects):
            print('{} / {}'.format(i, count))
            user.probable_spammer = False
            user.is_suspended = False
            user.paper_votes.update(is_removed=False)
            user.papers.update(is_removed=False)
            Thread.objects.filter(created_by=user).update(is_removed=True)
            Comment.objects.filter(created_by=user).update(is_removed=True)
            Reply.objects.filter(created_by=user).update(is_removed=True)
            user.save()