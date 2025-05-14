from django.contrib import admin
from .models import Post, Comment, Category, OneTimeCode


class PostAdmin(admin.ModelAdmin):
    list_display= ['title', 'user', 'category']

class CommentAdmin(admin.ModelAdmin):
    list_display= ['text', 'user', 'is_accepted']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(OneTimeCode)
