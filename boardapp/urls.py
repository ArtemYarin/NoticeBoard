from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import PostList, PostDetail, CreateComment, register_view, register_with_code_view, ProfilePage, accept_comment, CreatePost, UpdatePost, DeletePost


urlpatterns = [
    path('', PostList.as_view(), name='main_page'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/comment', CreateComment.as_view(), name='create_comment'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='main_page'), name='logout'),
    path('registration',  register_view, name='registration'),
    path('registration/confirmation', register_with_code_view, name='confirmation'),
    path('profile/<int:pk>', ProfilePage.as_view(), name='profile'),
    path('profile/accept/<int:comment_pk>', accept_comment, name='accept_comment'),
    path('post/create', CreatePost.as_view(), name='create_post'),
    path('post/edit/<int:pk>', UpdatePost.as_view(), name='update_post'),
    path('post/delete/<int:pk>', DeletePost.as_view(), name='delete_post'),
]