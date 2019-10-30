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
from django.contrib import messages

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
        
        mygroups_admin = Group.objects.filter(owner=request.user) 
        groups_owned = []
        for i in mygroups_admin:
            groups_owned.append(i.group_name)
        my_groups_member_group_name = []
        all_groups = Group.objects.all()
        for grp in all_groups:
            if request.user in grp.members.all():
                my_groups_member_group_name.append(grp.group_name)

        groups = Group.objects.filter(user_privacy='public')
        return render(request, 'Groups/group_home.html',{'groups':groups,'my_groups':groups_owned,'my_groups_members':my_groups_member_group_name,'mygroups_admin':mygroups_admin})
    messages.success(request, f'Login first')
    return redirect('login')


class Group_Create(LoginRequiredMixin,CreateView):
    model = Group
    fields = ['group_name','description','cost','user_privacy']
    template_name = 'Groups/create_group.html'
    context_object_name = 'groups'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        constraint = Constraint.objects.get(owner = self.request.user)
        if constraint.user_type == 'casual':
            messages.success(self.request, f'Casual user cannot make groups')
            return redirect('group_home')
        if constraint.user_type == 'silver':
            if constraint.number_of_groups < 2:
                constraint.number_of_groups+=1
                constraint.save()
                return super().form_valid(form)
            else:
                messages.success(self.request, f'Group Limit has exceeded')
                return redirect('group_home') 
        if constraint.user_type == 'gold':
            if constraint.number_of_groups < 4:
                constraint.number_of_groups+=1
                constraint.save()
                return super().form_valid(form)
            else:
                messages.success(self.request, f'Group limit has exceeded')
                return redirect('group_home')
        else:
            constraint.number_of_groups+=1
            constraint.save()
            return super().form_valid(form)


class Group_Update(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Group
    fields = ['description','cost','user_privacy']
    template_name = 'Groups/create_group.html'
    context_object_name = 'groups'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        constraint = Constraint.objects.get(owner = self.request.user)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

@login_required
def mygroup(request,group_name):
    if request.user.is_authenticated:
        group = Group.objects.get(group_name=group_name)
        requests = Group_join_request.objects.filter(group=group).exclude(user_requesting=group.owner).order_by('-date_posted')
        members = group.members.all()
        
        members_name = []
        for member in members:
            members_name.append(member.username)

        if request.user in group.members.all() or request.user == group.owner:
            group_posts = Group_post.objects.filter(group=group).order_by('-date_posted')
            return render(request,'Groups/mygroup.html',{'group_posts':group_posts,'members':members_name,'member_requests':requests,'group_name':group.group_name,'owner_name':group.owner.username})
        else:
            messages.success(request, f'You are not part of this group')
            return redirect('group_home')
    else:
        messages.success(request, f'Login first')
        return redirect('login')


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
    if request.user.is_authenticated:
        group = Group.objects.get(group_name = group_name)
        new_member = User.objects.get(pk=pk)
        wallet = Wallet.objects.get(owner=new_member)
        wallet_admin = Wallet.objects.get(owner=group.owner)
        if request.user == group.owner and wallet.money >= group.cost:
            print("before: ",wallet.money,wallet_admin.money,group.cost)
            wallet.money = wallet.money - group.cost
            wallet_admin.money = wallet_admin.money + group.cost
            wallet.save()
            wallet_admin.save()
            print("after: ",wallet.money,wallet_admin.money,group.cost)
            Group.add_member(group_name,new_member)
            join_request = Group_join_request.objects.get(group=group,user_requesting=new_member)
            join_request.delete()
            return redirect('group_home')
        else:
            if request.user != group.owner:
                messages.success(request, f'You are not the group admin')
                return redirect('group_home')
            elif wallet.money >= group.cost:
                messages.success(request, f'User cannot pay group joining cost')
                return redirect('group_home')
            else:
                return redirect('group_home')
    else:
        messages.success(request, f'Login first')
        return redirect('login')


@login_required
def remove_group_member(request,group_name,username):
    if request.user.is_authenticated:
        group = Group.objects.get(group_name = group_name)

        new_member = User.objects.get(username=username)
        
        if request.user == group.owner:
            Group.remove_member(group_name,new_member)    
            return redirect('group_home')
        else:
            messages.success(request, f'You are not the group admin')
            return redirect('group_home')
    else:
        messages.success(request, f'Login first')
        return redirect('login')
