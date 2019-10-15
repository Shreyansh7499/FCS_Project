from django.urls import path
from .views import Post_Create,Post_Update,Post_Delete
from . import views

urlpatterns = [
    path('', views.home, name='Wall-home'),
    path('create_post', Post_Create.as_view(), name='Wall-create-post'),
    path('update_post/<int:pk>/', Post_Update.as_view(), name='Wall-update-post'),
    path('delete_post/<int:pk>/', Post_Delete.as_view(), name='Wall-delete-post'),
]