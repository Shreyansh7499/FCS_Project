from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from model_utils import Choices


class Constraint(models.Model):
    owner = models.ForeignKey(User,related_name="owner_constraint",on_delete=models.CASCADE,unique=True)

    user_choices = Choices('casual', 'silver','gold','platinum','commercial')
    privacy_choices = Choices('private','public','friends')

    user_privacy = models.CharField(choices=privacy_choices, default=privacy_choices.private, max_length=20)
    user_type = models.CharField(choices=user_choices, default=user_choices.casual, max_length=20)
    number_of_transactions = models.IntegerField(default = 0)
    number_of_groups = models.IntegerField(default = 0)


    def __str__(self):
        return str(self.owner.username +" privacy_choices " + str(self.user_type) + " "+ str(self.number_of_groups) +" "+ str(self.number_of_transactions))

    def get_absolute_url(self):
        return reverse('Wall-home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)