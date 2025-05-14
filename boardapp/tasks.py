from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

import datetime

from NoticeBoard.settings import EMAIL_HOST_USER
from .models import OneTimeCode, Comment


@shared_task
def send_confirmation_code(code, email):
    send_mail(
                subject='Email confirmation',
                message=f'Confirmation code {code}',
                from_email=EMAIL_HOST_USER,
                recipient_list = [email]
            )
    
@shared_task
def delete_confirmation_code():
    time = datetime.datetime.now()
    time_to_delete = time - datetime.timedelta(minutes=5)
    OneTimeCode.objects.filter(created_at__lte=time_to_delete).delete()

@shared_task
def weekly_news():
    users = [user for user in User.objects.all()]
    send_mail(
        subject='Weekly news',
        message=f'This  week a lot of new posts was posted',
        from_email=EMAIL_HOST_USER,
        recipient_list = users
    )

@shared_task
def send_on_comment_created(comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    message = f'Post: {comment.post.title}\nUser: {comment.user.username}\nComment: {comment.text}'
    recipient = comment.post.user.email
    send_mail(
                subject='Your post was commented',
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list = [recipient]
            )

@shared_task
def comment_accepted(comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    send_mail(
        subject='Your comment was accepted',
        message=f'Your comment: {comment.text} was accepted',
        from_email=EMAIL_HOST_USER,
        recipient_list = [comment.user.email]
    )