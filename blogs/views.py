from django.shortcuts import render

from .models import Blog


def blog_list_view(request):
    blogs = Blog.objects.filter(status='pub')
    return render(request, 'blogs/blogs_list_page.html', context={'blogs': blogs})
