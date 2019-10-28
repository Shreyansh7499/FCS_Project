from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from .models import *
from Constraint.models import Constraint
from Wallet.models import Wallet
from django.contrib.auth import update_session_auth_hash


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
def profile(request,username):
    user = User.objects.get(username=username)
    constraint = Constraint.objects.get(owner=user)
    if constraint.user_privacy == 'public':
        return render(request,'Users/profile.html',{'profile_username':user.username})
    elif constraint.user_privacy == 'friends':
        data = get_friends_matrix(user)
        if request.user in data['friends']:
            return render(request,'Users/profile.html',{'profile_username':user.username})
    return render(request, 'Wall/home.html')


@login_required
def friend_page(request):
    if request.user.is_authenticated:
        data = get_friends_matrix(request.user)
        return render(request, 'Users/friends.html',data)
    return render(request, 'Wall/home.html')

def get_friends_matrix(user):
    user_friends = get_one_sided_friends(user)
    all_users = User.objects.exclude(id=user.id)
    friend_requests_received = []
    friend_requests_sent = []
    friends = []
    other_users = []
    for i in all_users:
        i_friends = get_one_sided_friends(i)

        if i_friends and user in i_friends:
            if user_friends and i in user_friends:
                friends.append(i)
            else:
                friend_requests_received.append(i)
        else:
            if user_friends and i in user_friends:
                friend_requests_sent.append(i)
            else:
                other_users.append(i)

    data = {'other_users':other_users,'friends':friends,'friend_requests_sent':friend_requests_sent,'friend_requests_received':friend_requests_received}
    return data

def get_one_sided_friends(user):
    try:
        friend = Friend.objects.get(current_user = user)
        friends = friend.users.all() 
    except Friend.DoesNotExist:
        friends = None
    return friends

def get_usernames(users):
    ret = []
    for i in users:
        ret.append(i)
    return ret

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

    