from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from Messages.views import get_friends_matrix
from Constraint.models import Constraint
from Wallet.models import Wallet
from django.contrib.auth.models import User
from django.contrib import messages


class Post_Create(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','wall_owner']
    template_name = 'Wall/create_post.html'
    context_object_name = 'posts'

    def form_valid(self,form):
        form.instance.author = self.request.user
        data = get_friends_matrix(form.instance.wall_owner)
        if self.request.user in data['friends'] or self.request.user == form.instance.wall_owner:
            return super().form_valid(form)
        else:
            messages.success(request, f'Cannot create post')
            return redirect('Wall-home')


class Post_Update(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','wall_owner']
    template_name = 'Wall/create_post.html'
    context_object_name = 'posts'

    def form_valid(self,form):
        form.instance.author = self.request.user
        data = get_friends_matrix(form.instance.wall_owner)
        if self.request.user in data['friends'] or self.request.user == form.instance.wall_owner:
            return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class Post_Delete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user == post.wall_owner:
            return True
        return False
    success_url = '/'



def home(request):
    if request.user.is_authenticated:
        try:
            constraint = Constraint.objects.get(owner=request.user)
        except Constraint.DoesNotExist:
            return redirect('create_constraint')
        try:
            wallet = Wallet.objects.get(owner=request.user)
        except Wallet.DoesNotExist:
            return redirect('wallet_create')    
        data = {'posts': Post.objects.filter(wall_owner = request.user).order_by('-date_posted')}	
        return render(request, 'Wall/home.html',data)
    messages.success(request, f'log in first')
    return redirect('login')


def friend_wall(request,username):
    if request.user.is_authenticated:
        friend = User.objects.get(username=username)
        data = get_friends_matrix(friend)
        if request.user in data['friends']:
            posts = {'posts': Post.objects.filter(wall_owner = friend).order_by('-date_posted')}
            return render(request, 'Wall/friend_wall.html',posts)
        else:
            messages.success(request, f'You are not his/her friend')
            return redirect('Wall-home')
    else:
        messages.success(request, f'log in first')
        return redirect('login')