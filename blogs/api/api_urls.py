from django.urls import path
from .api_views import (
    BlogListCreateAPIView, BlogRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('blogs/', BlogListCreateAPIView.as_view(), name='api-blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyAPIView.as_view(), name='api-blog-detail'),
    path('comments/', CommentListCreateAPIView.as_view(), name='api-comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='api-comment-detail'),
]
