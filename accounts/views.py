from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UserForm, UserLoginForm
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib import messages, auth


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.profile.city = form.cleaned_data.get('city')
        user.save()
        messages.success(request, 'You are registered! Please Log In!')
        return redirect("accounts:login")
    return render(request,'registration.html', {'user_form':form})

def user_login(request):
    un_form = UserLoginForm(request.POST or None)
    context = {'user_form':un_form}
    if un_form.is_valid():
        username = un_form.cleaned_data['username']
        password = un_form.cleaned_data['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("back:dashboard")
        else:
            messages.error(request, 'Login Failed!')
            return redirect('accounts:login')
    return render(request,'login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect('/')