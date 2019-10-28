from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	
	def __Str__(self):
		return f'{self.user.username}'

class Friend(models.Model):
	users = models.ManyToManyField(User)
	current_user = models.ForeignKey(User,related_name='owner',null=True,on_delete=models.CASCADE)
	
	@classmethod
	def add_friend(cls,current_user,new_friend):
		friend,created = cls.objects.get_or_create(current_user=current_user)
		friend.users.add(new_friend)

	#make it private ??
	@classmethod
	def remove_friend(cls,current_user,new_friend):
		friend,created = cls.objects.get_or_create(current_user=current_user)
		friend.users.remove(new_friend)