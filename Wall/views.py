from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class Post_Create(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'Wall/create_post.html'
    context_object_name = 'posts'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Post_Update(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'Wall/create_post.html'
    context_object_name = 'posts'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class Post_Delete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    success_url = '/Wall'



def home(request):
	if request.user.is_authenticated:
		data = {'posts': Post.objects.filter(author = request.user).order_by('-date_posted')}	
		return render(request, 'Wall/home.html',data)
	return render(request, 'Wall/home.html')



@login_required
def create_post(request):
    if request.method == 'POST':
        form = create_post_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('Wall-home')
    else:
        form = create_post_form()
    return render(request, 'Wall/create_post.html', {'form': form})

