from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import *
from .models import *

# Create your views here.

def index(request):
    greeting = ''
    if request.user.is_authenticated:
        if request.user.gender == 'male':
            greeting = 'Здравствуйте, мой господин!'
        elif request.user.gender == 'female':
            greeting = 'Здравствуйте, моя госпожа!'
    return render(request, 'index.html', {'greeting': greeting})


def profile(request, status):
    if status == 'all':
        my_app_list = Aplication.objects.filter(user=request.user.pk).order_by('-date')
    else:
        my_app_list = Aplication.objects.filter(status=status).order_by('-date')
    return render(request, 'profile.html', context={'my_app_list': my_app_list})

def app_filter(request, status):
    app_list = Aplication.objects.filter(status=status).order_by('-date')
    return render(request, 'profile.html', context={'app_list': app_list, 'status': status})

def delete_request(request, request_id):
    request_obj = Aplication.objects.get(id=request_id)
    if request.method == 'POST':
        request_obj.delete()
        return redirect(reverse('profile', kwargs={'status': 'all'}))
    else:
        request_obj.delete()
        return redirect(reverse('app_list'))

def registration(request):
    if request.method == 'POST':
        form = Reg_Form(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.confirm_password = 'NULL'
            new_user = form.save()
            return render(request, 'index.html')
    else:
        form = Reg_Form()

    return render(request, 'registration/registration.html', {'form': form})

class Login(LoginView):
    template_name = 'registration/login.html'

