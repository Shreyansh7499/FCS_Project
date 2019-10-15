from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Wall-home'),
    path('create_post', views.create_post, name='Wall-create-post'),

]