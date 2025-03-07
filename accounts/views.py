from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .models import CustomUserModel
from .forms import CustomUserCreateForm


def signup_view(request):
    if request.method == 'POST':  
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreateForm()

    return render(request, 'registration/signup_page.html', {'form': form})  
