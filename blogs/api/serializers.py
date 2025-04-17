# serializers.py
from rest_framework import serializers
from blogs.models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'is_active', 'created_datetime']

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'user', 'body', 'status', 
            'created_datetime', 'modfied_datetime', 'comments'
        ]