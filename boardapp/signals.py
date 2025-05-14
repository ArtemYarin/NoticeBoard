from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment
from .tasks import send_on_comment_created


@receiver(post_save, sender = Comment)
def comment_created(sender, instance, created,  **kwargs):
    if created:
        send_on_comment_created.delay(comment_pk=instance.pk)
