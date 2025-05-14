from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = CKEditor5Field('Text', config_name='extends')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('main_page')

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    is_accepted = models.BooleanField(blank=True, default=False)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.post.pk})

    def __str__(self):
        return self.text[:50]


class Category(models.Model):
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name.title()
    

class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
