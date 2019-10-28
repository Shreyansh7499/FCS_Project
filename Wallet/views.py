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

@login_required
def wallet_home(request):
    if request.user.is_authenticated:
        try:
            constraint = Constraint.objects.get(owner=request.user)
        except Constraint.DoesNotExist:
            return redirect('create_constraint')
        try:
            wallet = Wallet.objects.get(owner=request.user)
            transactions = Transaction.objects.filter(receiver=request.user)
            return render(request, 'Wallet/wallet_home.html',{'money':wallet.money,'transactions':transactions})
        except Wallet.DoesNotExist:
            return redirect('wallet_create') 
    return render(request, 'Wallet/wallet_home.html')


class Wallet_Create(LoginRequiredMixin,CreateView):
    model = Wallet
    fields =[]
    template_name = 'Wallet/create_wallet.html'
    context_object_name = 'wallet'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        if Wallet.objects.filter(owner=self.request.user).count() == 0:
        	return super().form_valid(form)
        else:
            return redirect('wallet_home')


class Transaction_Create(LoginRequiredMixin,CreateView):
    model = Transaction
    fields = ['receiver','amount']
    template_name = 'Wallet/create_transaction.html'
    context_object_name = 'transaction'

    def form_valid(self,form):
        form.instance.sender = self.request.user
        transactions = Transaction.objects.filter(sender=self.request.user)
        total_pending = 0
        for transaction in transactions:
            total_pending += int(transaction.amount)
        total_pending += int(form.instance.amount)

        constraint = Constraint.objects.get(owner=self.request.user)
        if constraint.user_type == 'casual':
            max_transaction = 15
        elif constraint.user_type == 'commercial':
            max_transaction = -1
        else:
            max_transaction = 30

        if max_transaction == -1:

            if Wallet.objects.get(owner = self.request.user).money >= int(total_pending) and int(form.instance.amount)>0:
                constraint.number_of_transactions+=1
                constraint.save()
                return super().form_valid(form)
            else:
                return redirect('wallet_home')
        else:
            if Wallet.objects.get(owner = self.request.user).money >= int(total_pending) and int(form.instance.amount)>0 and max_transaction>constraint.number_of_transactions:
                constraint.number_of_transactions+=1
                constraint.save()
                return super().form_valid(form)
            else:
                return redirect('wallet_home')


def accept_transaction(request,pk):
	transaction = Transaction.objects.get(pk=pk)
	wallet_sender = Wallet.objects.get(owner=transaction.sender)
	wallet_receiver = Wallet.objects.get(owner=transaction.receiver)	

	if request.user == transaction.receiver:
		if wallet_sender.money >= int(transaction.amount):
			wallet_sender.money = wallet_sender.money - int(transaction.amount)
			wallet_receiver.money = wallet_receiver.money + int(transaction.amount)
			wallet_receiver.save()
			wallet_sender.save()
			Transaction_Log.objects.create(sender=transaction.sender,receiver=transaction.receiver,amount=transaction.amount)
			transaction.delete()
	
	return redirect('wallet_home')


class Add_Money_Transaction_Create(LoginRequiredMixin,CreateView):
    model = Add_Money_Transaction
    fields = ['amount']
    template_name = 'Wallet/create_add_money_transaction.html'
    context_object_name = 'add_money_transaction'

    def form_valid(self,form):
        form.instance.sender = self.request.user
        amount = int(form.instance.amount)
        if amount > 0:
        	wallet = Wallet.objects.get(owner=self.request.user)
        	wallet.money = wallet.money + amount
        	wallet.save()
        	return super().form_valid(form)
        else:
        	return redirect('wallet_home')
