import django_filters
from django.db import models
from .models import Post


class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    tag = django_filters.CharFilter(field_name='tags__slug')
    author = django_filters.NumberFilter(field_name='author__id')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Post
        fields = ['status', 'category', 'tag', 'author', 'is_featured']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(content__icontains=value)
        )
