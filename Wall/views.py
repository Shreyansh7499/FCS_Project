from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class create_post_form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)


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


@login_required
def update_post(request,id):
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

# @login_required
# def delete_post(request,id):
#     post = get_object_or_404(Post,id=id)
#     if request.user == post.user:
#         post.delete()
#         return redirect('Wall-home')
#     else:
#         raise PermissionDenied
#         return redirect('Wall-home')