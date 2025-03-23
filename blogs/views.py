from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Blog
from .forms import BlogForm
from .decorators import user_is_authorized
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def blog_list_view(request):
    blogs_list = Blog.objects.filter(status='pub')
    paginator = Paginator(blogs_list, 7) 

    page = request.GET.get('page')  # Get the current page number from the request
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blogs/blogs_list_page.html', context={'blogs': blogs})

@login_required
def blog_detail_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blogs/blog_detail_page.html', context={'blog': blog})


@login_required
def blog_create_view(request):
    if request.method == 'POST':
        form = BlogForm(data=request.POST)
        if form.is_valid:
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()

            return redirect(new_form.get_absolute_url())
    else:
        form = BlogForm()
    
    return render(request, 'blogs/blog_create_page.html', context={'form': form})


@login_required
@user_is_authorized
def blog_update_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(data=None or request.POST, instance=blog)
        if form.is_valid():
            form.save()

        return redirect(Blog.get_absolute_url(blog))
    
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogs/blog_update_page.html', context={'form': form, 'blog': blog})


@login_required
@user_is_authorized
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    
    return render(request, 'blogs/blog_delete_page.html', context={'blog': blog})