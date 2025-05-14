from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

import random
import string

from .models import Post, Comment, OneTimeCode
from .forms import BaseRegisterForm, PostForm, CommentForm
from NoticeBoard.settings import EMAIL_HOST_USER
from .tasks import send_confirmation_code, comment_accepted
from .filters import CommentFilter


# Register
def register_view(request):
    if not request.user.id == None:
        return redirect('main_page')
    
    if request.method == "POST":
        form = BaseRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            email=form.cleaned_data['email']
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            OneTimeCode.objects.create(user=user, code=code)

            send_confirmation_code.delay(code=code, email=email)
            return redirect('confirmation')

    form = BaseRegisterForm()
    return render(request, 'register.html', {'form': form})


def register_with_code_view(request):
    if not request.user.id == None:
        return redirect('main_page')
    
    if request.method == "POST":
        username = request.POST['username']
        code = request.POST['code']

        if OneTimeCode.objects.filter(user__username=username, code=code).exists():
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return render(request, 'success_register.html')

    return render(request, 'register_code.html')
    

class ProfilePage(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        posts = user.post_set.all()
        comments = Comment.objects.filter(post__user=user)

        self.filterset = CommentFilter(self.request.GET, comments, request=self.request.user)
        comments = self.filterset.qs

        context['filterset'] = self.filterset

        context['posts'] = posts
        context['comments'] = comments
        return context
    

def accept_comment(request, comment_pk):
    if comment_pk is None:
        return redirect('/')

    comment = Comment.objects.get(pk=comment_pk)

    comment.is_accepted = not comment.is_accepted
    comment.save()
    comment_accepted.delay(comment.pk)

    return redirect('profile', pk=request.user.pk)


# Post view
class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comment_set.all()
        context['comments'] = comments
        return context


# Post change
class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class UpdatePost(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = PostForm


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('main_page')


# Comment
class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    