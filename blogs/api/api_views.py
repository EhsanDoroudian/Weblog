from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from blogs.models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class BlogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'user']

    def get_queryset(self):
        queryset = Blog.objects.select_related('user')
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='pub')
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Blog.objects.select_related('user')

class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_active=True).select_related('user', 'blog')
        blog_id = self.request.query_params.get('blog')
        if blog_id:
            if not Blog.objects.filter(id=blog_id).exists():
                raise serializers.ValidationError("Invalid blog_id.")
            queryset = queryset.filter(blog_id=blog_id)
        return queryset

    def perform_create(self, serializer):
        blog_id = self.request.data.get('blog')
        blog = Blog.objects.filter(id=blog_id, status='pub').first()
        if not blog:
            raise serializers.ValidationError("Cannot comment on unpublished blogs.")
        serializer.save(user=self.request.user, blog=blog)

class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Comment.objects.select_related('user', 'blog')

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.is_active = False  # Soft delete
        comment.save()
        return Response(status=204)