# serializers.py
from rest_framework import serializers
from blogs.models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    blog = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'text', 'is_active', 'created_datetime']
    
    def create(self, validated_data):
        blog_id = self.context["blog_pk"]
        return Comment.objects.create(blog_id=blog_id, **validated_data)

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'user', 'body', 'status', 
            'created_datetime', 'modified_datetime', 'comments'
        ]