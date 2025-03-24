from django.urls import reverse
from django.db import models
from accounts.models import CustomUserModel


class Blog(models.Model):
    STATUS_CHOICES = (
        ('pub', 'publish'),
        ('drf', 'draft'),
    )
    title = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='blogs')
    body = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modfied_datetime = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=3)


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.id])
    


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modfied_datetime = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.text
    
