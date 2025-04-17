from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blogs.models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # custom permission

# BLOG APIs
class BlogListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Blog.objects.all()
        return Blog.objects.filter(status='pub')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Blog.objects.all()


# COMMENT APIs
class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.filter(is_active=True)
        blog_id = self.request.query_params.get('blog')
        if blog_id:
            queryset = queryset.filter(blog_id=blog_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
