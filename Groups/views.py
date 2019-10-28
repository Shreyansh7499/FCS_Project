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
from Constraint.models import Constraint
from Wallet.models import Wallet


@login_required
def group_home(request):
    if request.user.is_authenticated:
        try:
            constraint = Constraint.objects.get(owner=request.user)
        except Constraint.DoesNotExist:
            return redirect('create_constraint')
        try:
            wallet = Wallet.objects.get(owner=request.user)
        except Wallet.DoesNotExist:
            return redirect('wallet_create')

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
        constraint = Constraint.objects.get(owner = self.request.user)
        if constraint.user_type == 'casual':
            return redirect('group_home')
        if constraint.user_type == 'silver':
            if constraint.number_of_groups < 2:
                constraint.number_of_groups+=1
                constraint.save()
                return super().form_valid(form)
            else:
                return redirect('group_home') 
        if constraint.user_type == 'gold':
            if constraint.number_of_groups < 4:
                constraint.number_of_groups+=1
                constraint.save()
                return super().form_valid(form)
            else:
                return redirect('group_home')
        else:
            constraint.number_of_groups+=1
            constraint.save()
            return super().form_valid(form)
        # data = get_friends_matrix(self.request.user)
        # friend = form.instance.receiver
        # print(friend)
        # if friend in data['friends']:
        # else:
        #     return redirect('messages_view')


@login_required
def mygroup(request,group_name):
    group = Group.objects.filter(group_name=group_name)[0]
    requests = Group_join_request.objects.filter(group=group).exclude(user_requesting=group.owner).order_by('-date_posted')
    members = group.members.all()

    if request.user in group.members.all() or request.user == group.owner:
        group_posts = Group_post.objects.filter(group=group).order_by('-date_posted')
        return render(request,'Groups/mygroup.html',{'group_posts':group_posts,'members':members,'member_requests':requests,'group_name':group.group_name,'owner_name':group.owner.username})
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
        if self.request.user in members or self.request.user == group.owner:
            return super().form_valid(form)
        else:
            return redirect('group_home')


class Group_Join_request_Create(LoginRequiredMixin,CreateView):
    model = Group_join_request
    fields = ['group']
    template_name = 'Groups/create_group_join_request.html'
    context_object_name = 'group_join_request'

    def form_valid(self,form):
        form.instance.user_requesting = self.request.user

        if Group_join_request.objects.filter(group=form.instance.group,user_requesting=self.request.user).count() >= 1 and self.request.user.username != form.instance.group.owner.username:
            return redirect('group_home')
        else:
            return super().form_valid(form)


@login_required
def add_group_member(request,group_name,pk):
    group = Group.objects.get(group_name = group_name)
    new_member = User.objects.get(pk=pk)

    if request.user == group.owner:
        Group.add_member(group_name,new_member)
        join_request = Group_join_request.objects.get(group=group,user_requesting=new_member)
        join_request.delete()
    return redirect('group_home')


@login_required
def remove_group_member(request,group_name,pk):
    group = Group.objects.get(group_name = group_name)
    new_member = User.objects.get(pk=pk)
    
    if request.user == group.owner:
        Group.remove_member(group_name,new_member)    
    return redirect('group_home')
