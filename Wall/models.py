from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='post_author')
    wall_owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_wall_owner')

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Wall-home')

    def form_valid(self, form):
    	form.instance.created_by = self.request.user
    	return super().form_valid(form)