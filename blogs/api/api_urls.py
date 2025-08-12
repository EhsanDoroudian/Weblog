from django.urls import path
from . import api_views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('blogs', api_views.BlogViewSet, basename='blog')
router.register('comments', api_views.CommentViewSet, basename='comment')


blogs_router = routers.NestedDefaultRouter(parent_router=router, parent_prefix='blogs', lookup='blog')
blogs_router.register('comments', api_views.CommentViewSet, basename='blog-comments')

urlpatterns = router.urls + blogs_router.urls