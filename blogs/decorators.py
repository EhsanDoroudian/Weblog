from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps
from .models import Blog


def user_is_authorized(view_func):
    """
    Custom decorator to check if the user is a superuser, staff, or the creator of the blog.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])  # Use get_object_or_404 to handle non-existent blogs
        if request.user.is_superuser or request.user.is_staff or request.user == blog.user:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to access this page.")
    return _wrapped_view