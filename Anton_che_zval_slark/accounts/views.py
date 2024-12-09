from django.shortcuts import render
from .forms import *
from django.contrib.auth.views import LoginView
# Create your views here.

def index(request):
    return render(request, 'index.html')


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