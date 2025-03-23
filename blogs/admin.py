from django.contrib import admin
from .models import Blog, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_datetime', 'status']
    ordering = ('-modfied_datetime',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'blog', 'is_active']
    ordering = ('-modfied_datetime',)

