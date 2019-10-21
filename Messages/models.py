from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Message(models.Model):

    message = models.TextField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receiver',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.message +" by: " + self.sender.username + ". from:" + self.receiver.username)

    def get_absolute_url(self):
        return reverse('messages_view')

    def form_valid(self, form):
    	form.instance.created_by = self.request.user
    	return super().form_valid(form)