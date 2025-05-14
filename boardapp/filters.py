from django_filters import FilterSet, ModelChoiceFilter
from .models import Comment, Post


class CommentFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs['request']
        self.filters['post'].queryset = Post.objects.filter(user=self.user)

    class Meta:
        model = Comment
        fields = ['post']
        