from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def group_home(request):
	if request.user.is_authenticated:
		groups = Group.objects.all()
		return render(request, 'Groups/group_home.html',{'groups':groups})
	return render(request, 'Groups/group_home.html')


class Group_Create(LoginRequiredMixin,CreateView):
    model = Group
    fields = ['group_name','description']
    template_name = 'Groups/create_group.html'
    context_object_name = 'groups'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        # data = get_friends_matrix(self.request.user)
        # friend = form.instance.receiver
        # print(friend)
        # if friend in data['friends']:
        return super().form_valid(form)
        # else:
        #     return redirect('messages_view')


@login_required
def create_group(request):
    if request.method == 'POST':
        form = create_post_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sender = request.user
            post.save()
            return redirect('group_home')
    else:
        form = create_post_form()
    return render(request, 'Group/create_group.html', {'form': form})

@login_required
def mygroup(request,group_name):
    group = Group.objects.filter(group_name=group_name)[0]
    if request.user in group.members.all():
        group_posts = Group_post.objects.filter(group=group).order_by('-date_posted')
        return render(request,'Groups/mygroup.html',{'group_posts':group_posts})
    else:
        return redirect('group_home')


class Group_Post_Create(LoginRequiredMixin,CreateView):
    model = Group_post
    fields = ['message','group']
    template_name = 'Groups/create_group_post.html'
    context_object_name = 'group_post'

    def form_valid(self,form):
        form.instance.sender = self.request.user
        group = form.instance.group
        members = group.members.all()
        if self.request.user in members:
            return super().form_valid(form)
        else:
            return redirect('group_home')


@login_required
def create_group_post(request):
    if request.method == 'POST':
        form = create_post_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sender = request.user
            post.save()
            return redirect('group_home')
    else:
        form = create_post_form()
    return render(request, 'Group/create_group_post.html', {'form': form})
