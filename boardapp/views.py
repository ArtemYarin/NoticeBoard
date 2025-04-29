from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from .models import Post, Comment
from .forms import BaseRegisterForm, PostForm, CommentForm

# Register
class RegisterView(CreateView):
    model = User
    success_url = '/'
    form_class = BaseRegisterForm

class ProfilePage(DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        posts = user.post_set.all()
        comments = []
        for post in posts:
            comments.append(post.comment_set.all())

        context['posts'] = posts
        context['comments'] = comments
        return context
    

def accept_comment(request, comment_pk=None, user_pk=None):
    if not comment_pk or user_pk:
        return redirect('/')

    comment = Comment.objects.get(pk=comment_pk)
    comment.is_accepted = True
    return redirect(f'profile/{user_pk}')


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
class CreatePost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeletePost(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('main_page')


# Comment
class ListComment(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'comments.html'


class CreateComment(CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


def accept_comment(request):
    pass
