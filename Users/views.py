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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


# class Fakeuser_Login_Create(LoginRequiredMixin,CreateView):
#     model = Fakeuser
#     fields = ['user']
#     template_name = 'Wallet/create_add_money_transaction.html'
#     context_object_name = 'fakeuser'

#     def form_valid(self,form):

#         otp = generate_OTP()
#         try:
#             otp_object = Fakeuser.objects.get(owner=form.instance.user)
#         except:
#             otp_object = Fakeuser.objects.create(owner=form.instance.user)
#         otp_object.otp = otp
#         otp_object.save()

#         send_mail(
#                 subject="Your OTP Password",
#                 message="Your OTP password is %s" % otp,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[form.instance.user.email]
#             )


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
            print(form.instance.username,"username")
            new_user = User.objects.get(username = form.instance.username)
            wallet = Wallet.objects.create(owner=new_user)
            wallet.save()
            constraint = Constraint.objects.create(owner=new_user)
            constraint.save()
            messages.success(request, f'Login please')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'Users/register.html', {'form': form})

@login_required
def profile(request,username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        constraint = Constraint.objects.get(owner=user)

        if constraint.user_privacy == 'public' or request.user.username == username:
            return render(request,'Users/profile.html',{'profile_username':user.username,'profile_email':user.email})
        elif constraint.user_privacy == 'friends':
            data = get_friends_matrix(user)
            if request.user in data['friends']:
                return render(request,'Users/profile.html',{'profile_username':user.username,'profile_email':user.email})
        messages.success(request, f'The profile is private')
        return render(request, 'Wall/home.html')
    else:
        messages.success(request, f'Login first')
        return redirect('login')


@login_required
def friend_page(request):
    if request.user.is_authenticated:
        data = get_friends_matrix(request.user)
        return render(request, 'Users/friends.html',data)
    else:
        messages.success(request, f'Login first')
        return redirect('login')

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
    if request.user.is_authenticated:
        new_friend = User.objects.get(pk=pk)
        Friend.add_friend(request.user,new_friend)
        return redirect('friend_page')
    else:
        messages.success(request, f'Login first')
        return redirect('login')

@login_required
def remove_friend(request,pk):
    if request.user.is_authenticated:
        new_friend = User.objects.get(pk=pk)
        Friend.remove_friend(request.user,new_friend)
        return redirect('friend_page')   
    else:
        messages.success(request, f'Login first')
        return redirect('login')   

    