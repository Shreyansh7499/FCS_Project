from .models import Message
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from Users.views import get_friends_matrix
from django.contrib.auth.models import User
from django.db.models import Q
from Constraint.models import Constraint
from Wallet.models import Wallet


class Message_Create(LoginRequiredMixin,CreateView):
    model = Message
    fields = ['message','receiver']
    template_name = 'Messages/create_message.html'
    context_object_name = 'messages'

    def form_valid(self,form):
        form.instance.sender = self.request.user
        constraint = Constraint.objects.get(owner = self.request.user)
        if constraint.user_type == 'commercial':
            return super().form_valid(form)
        else:
            data = get_friends_matrix(self.request.user)
            friend = form.instance.receiver
            if friend in data['friends']:
                return super().form_valid(form)
            else:
                return redirect('messages_view')


def message_view(request):
	if request.user.is_authenticated:
		data = get_friends_matrix(request.user)	
		return render(request, 'Messages/message_view.html',data)
	return render(request, 'Messages/message_view.html')


@login_required
def chat(request,username):
    friend = User.objects.get(username = username)
    data = get_friends_matrix(request.user)
    if friend in data['friends']:
        messages = Message.objects.filter(Q(sender=friend,receiver=request.user) | Q(sender=request.user,receiver=friend)).order_by('date_posted')
        return render(request,'Messages/chat.html',{'messages':messages})
    else:
        return render(request,'Messages/message_view.html',{'messages':messages})
