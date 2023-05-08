from django.shortcuts import render, redirect
from .models.auth import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


@login_required(login_url='signin/')



def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    context = {
        'form': form,
    }

    return render(request, 'core/sign_in.html', context)

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, 'core/sign_up.html', context)




                                  
def logout_view(request):
    logout(request)
    return redirect('/')
