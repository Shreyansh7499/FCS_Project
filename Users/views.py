from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request,'Users/profile.html')


@login_required
def friend_page(request):
    if request.user.is_authenticated:
        all_users = User.objects.exclude(id=request.user.id)
        try:
            friend = Friend.objects.get(current_user = request.user)
            friends = friend.users.all() 
        except Friend.DoesNotExist:
            friends = None
        data = {'users':all_users,'friends':friends}   
        return render(request, 'Users/friends.html',data)
    return render(request, 'Wall/home.html')


@login_required
def add_friend(request,pk):
    new_friend = User.objects.get(pk=pk)
    Friend.add_friend(request.user,new_friend)
    return redirect('friend_page')

@login_required
def remove_friend(request,pk):
    new_friend = User.objects.get(pk=pk)
    Friend.remove_friend(request.user,new_friend)
    return redirect('friend_page')      

    