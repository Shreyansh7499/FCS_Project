from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Wallet(models.Model):
    owner = models.ForeignKey(User,related_name="owner_wallet",on_delete=models.CASCADE)
    money = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.owner.username +" by: " + str(self.money))

    def get_absolute_url(self):
        return reverse('wallet_home')

    def form_valid(self, form):
    	form.instance.created_by = self.request.user
    	return super().form_valid(form)


class Transaction(models.Model):
	sender = models.ForeignKey(User,related_name='transaction_sender',on_delete=models.CASCADE)
	receiver = models.ForeignKey(User,related_name='transaction_receiver',on_delete=models.CASCADE)
	amount = models.IntegerField(default = 0)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.sender.username +" to: "+ self.receiver.username + " amount:" + str(self.amount))

	def get_absolute_url(self):
		return reverse('wallet_home')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

class Add_Money_Transaction(models.Model):
	sender = models.ForeignKey(User,related_name='add_money_transaction_sender',on_delete=models.CASCADE)
	amount = models.IntegerField(default = 0)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.sender.username + " amount:" + str(self.amount))

	def get_absolute_url(self):
		return reverse('wallet_home')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

class Transaction_Log(models.Model):
	sender = models.ForeignKey(User,related_name='transaction_log_sender',on_delete=models.CASCADE)
	receiver = models.ForeignKey(User,related_name='transaction_log_receiver',on_delete=models.CASCADE)
	amount = models.IntegerField(default = 0)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.sender.username +" to: "+ self.receiver.username + " amount:" + str(self.amount))

	def get_absolute_url(self):
		return reverse('wallet_home')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)