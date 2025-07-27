from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import Blog
from .forms import BlogForm, CommentForm
from .decorators import user_is_authorized


def blog_list_view(request):
    blogs_list = Blog.objects.select_related('user').filter(status='pub').order_by('modfied_datetime')
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
    blog = get_object_or_404(
        Blog.objects.select_related('user').prefetch_related(
            'comments__user'
        ), 
        pk=pk
    )
    comment_form = CommentForm(request.POST)

    return render(request, 'blogs/blog_detail_page.html', context={'blog': blog, 'comment_form': comment_form})


@login_required
def blog_comment_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_form = comment_form.save(commit=False)
        new_form.blog = blog
        new_form.user = request.user
        new_form.save()
        return redirect(blog.get_absolute_url())

    return render(request, template_name='blogs/blog_detail_page.html',)


@login_required
def blog_create_view(request):
    if request.method == 'POST':
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()

            return redirect(new_form.get_absolute_url())
    else:
        form = BlogForm()
    
    return render(request, 'blogs/blog_create_page.html', context={'form': form})


@user_is_authorized
@login_required
def blog_update_view(request, pk):
    try:
        blog = Blog.objects.select_related('user').get(id=pk)
    except ObjectDoesNotExist:
        raise Http404("Blog post not found") 
    if request.method == 'POST':
        form = BlogForm(data=None or request.POST, instance=blog)
        if form.is_valid():
            form.save()

        return redirect(Blog.get_absolute_url(blog))
    
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogs/blog_update_page.html', context={'form': form, 'blog': blog})


@user_is_authorized
@login_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog.objects.select_related('user'), pk=pk)
    
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    
    return render(request, 'blogs/blog_delete_page.html', context={'blog': blog})