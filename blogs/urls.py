from django.urls import path

from . import views


urlpatterns = [
    path('', view=views.blog_list_view, name='blog_list'),
    path('<int:pk>/', view=views.blog_detail_view, name='blog_detail'),
    path('create/', view=views.blog_create_view, name='blog_create'),
    path('update/<int:pk>/',view=views.blog_update_view, name='blog_update'),
]
