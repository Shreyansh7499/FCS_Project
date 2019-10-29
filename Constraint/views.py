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
from Wallet.models import Wallet

class Constraint_Create(LoginRequiredMixin,CreateView):
    model = Constraint
    fields = ['user_privacy']
    template_name = 'Constraint/create_constraint.html'
    context_object_name = 'constraint'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        # data = get_friends_matrix(self.request.user)
        # friend = form.instance.receiver
        # print(friend)
        # if friend in data['friends']:
        return super().form_valid(form)
        # else:
        #     return redirect('messages_view')


class Constraint_Update(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Constraint
    fields = ['user_privacy','user_type']
    template_name = 'Constraint/update_constraint.html'
    context_object_name = 'constraint'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        constraint = Constraint.objects.get(owner=self.request.user)
        
        ll = ['casual', 'silver','gold','platinum','commercial']
        index_before = ll.index(constraint.user_type)
        index_after = ll.index(form.instance.user_type)

        print(index_before,index_after)
        wallet = Wallet.objects.get(owner = self.request.user)
        if form.instance.user_type == 'casual':
            pass
        elif form.instance.user_type == 'silver' and index_after >index_before:
            if wallet.money >= 50:
                wallet.money = wallet.money - 50
                wallet.save()
                print("silver")
            else:
                return redirect('Wall-home')
        elif form.instance.user_type == 'gold' and index_after >index_before:
            if wallet.money >= 100:
                wallet.money = wallet.money -100
                wallet.save()
                print("gold")
            else:
                return redirect('Wall-home')
        elif form.instance.user_type == 'platinum' and index_after >index_before:
            if wallet.money >= 150:
                wallet.money = wallet.money - 150
                wallet.save()
                print("platinum")
            else:
                return redirect('Wall-home')
        elif index_after >index_before:
            if wallet.money >= 5000 :
                wallet.money = wallet.money - 5000
                wallet.save()
                print("commercial")
            else:
                return redirect('Wall-home')
        # data = get_friends_matrix(self.request.user)
        # friend = form.instance.receiver
        # print(friend)
        # if friend in data['friends']:
        return super().form_valid(form)
        # else:
        #     return redirect('messages_view')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False


@login_required
def update_constraint(request):
    if request.user.is_authenticated:
        print(request.user.username,request.user.pk)
        user = User.objects.get(pk=request.user.pk)
        try:
            constraint = Constraint.objects.get(owner=request.user)
        except Constraint.DoesNotExist:
            return redirect('create_constraint')
        try:
            wallet = Wallet.objects.get(owner=request.user)
        except Wallet.DoesNotExist:
            return redirect('wallet_create')
        return redirect('update_constraint',pk=constraint.pk)
    else:
        return redirect('login')
