from django.utils import timezone
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Category, Tag
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostWriteSerializer,
    CommentSerializer, CategorySerializer, TagSerializer, UserSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category__slug', 'is_featured', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_at', 'views_count']

    def get_serializer_class(self):
        if self.action in ['list', 'featured', 'related']:
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Post.objects.all()

        if self.action in ['list', 'featured', 'related']:
            return Post.objects.filter(status='published')

        return Post.objects.filter(status='published') | Post.objects.filter(author=user)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
            post.save()

    def perform_update(self, serializer):
        post = serializer.save()
        if post.status == 'published' and not post.published_at:
            post.published_at = timezone.now()
            post.save()

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        post = self.get_object()
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return Response({'views_count': post.views_count})

    @action(detail=False, methods=['get'])
    def featured(self, request):
        posts = Post.objects.filter(status='published', is_featured=True)[:5]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        post = self.get_object()
        related = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id)[:3]
        serializer = PostListSerializer(related, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'is_approved']

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
