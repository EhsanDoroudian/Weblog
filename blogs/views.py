from django.shortcuts import render, get_object_or_404

from .models import Blog


def blog_list_view(request):
    blogs = Blog.objects.filter(status='pub')
    return render(request, 'blogs/blogs_list_page.html', context={'blogs': blogs})


def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blogs/blog_detail_page.html', context={'blog': blog})
