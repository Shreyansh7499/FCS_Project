from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Group(models.Model):
    owner = models.ForeignKey(User,related_name="owner_group",on_delete=models.CASCADE)
    description = models.TextField(max_length=100,null=True,blank=True)
    date_posted = models.DateTimeField(default=timezone.now,null=True,blank=True)
    group_name = models.TextField(max_length=100,unique=True)
    members = models.ManyToManyField(User,null=True,blank=True)
    
    def __str__(self):
        return str(self.group_name +" by: " + self.owner.username)

    def get_absolute_url(self):
        return reverse('group_home')

    def form_valid(self, form):
    	form.instance.created_by = self.request.user
    	return super().form_valid(form)


class Group_post(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    message = models.TextField(max_length=100)
    sender = models.ForeignKey(User,related_name="group_sender",on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now,null=True,blank=True)

    def __str__(self):
        return str(self.message +" by: " + self.sender.username)

    def get_absolute_url(self):
        return reverse('group_home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)