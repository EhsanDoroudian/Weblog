from rest_framework import generics, serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from blogs.models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly



class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'user']
    ordering_fields = ['modfied_datetime', 'created_datetime']
    filterset_fields = ['user', 'title', 'status']

    def get_queryset(self):
        return Blog.objects.select_related('user').prefetch_related(
            Prefetch('comments', queryset=Comment.objects.select_related('user'))
            )
            
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        blog_pk = self.kwargs['blog_pk']
        return Comment.objects.select_related('user', 'blog').filter(blog_id=blog_pk).all()
    
    def get_serializer_context(self):
        return {'blog_pk': self.kwargs["blog_pk"]}

    def perform_create(self, serializer):
        blog_id = self.kwargs["blog_pk"]
        blog = Blog.objects.filter(id=blog_id, status='pub').first()
        serializer.save(user=self.request.user, blog=blog)
