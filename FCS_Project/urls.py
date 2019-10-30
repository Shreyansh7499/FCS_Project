"""FCS_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include,reverse_lazy
from Users import views as user_view
from django.contrib.auth import views as auth_view
from Messages import views as messages_view
from Groups import views as group_view
from Wallet import views as wallet_view
from Wall import views as post_view
from Messages.views import Message_Create
from Constraint import views as constraint_view
from Groups.views import Group_Create,Group_Post_Create,Group_Join_request_Create,Group_Update
from Wallet.views import Wallet_Create,Transaction_Create,Add_Money_Transaction_Create
from Wall.views import Post_Create,Post_Update,friend_wall,Post_Delete
from Constraint.views import Constraint_Create,Constraint_Update
# from django_otp.forms import OTPAuthenticationForm
from Users.forms import OTPAuthentication
from django.conf.urls import url
from Users.views import SimpleOTPRegistrationForm


urlpatterns = [
    path('bleh_admin/', admin.site.urls),

    
    path('create_constraint', Constraint_Create.as_view(), name='create_constraint'),
    path('update_constraint/<int:pk>/', Constraint_Update.as_view(), name='update_constraint'),
    path('update_constraint_start/',constraint_view.update_constraint,name='update_constraint_start'),
    

    
    path('', post_view.home, name='Wall-home'),
    path('create_post', Post_Create.as_view(), name='Wall-create-post'),
    path('update_post/<int:pk>/', Post_Update.as_view(), name='Wall-update-post'),
    path('delete_post/<int:pk>/', Post_Delete.as_view(success_url=reverse_lazy('Wall-home')), name='delete_post'),
    path('friend_wall/<str:username>/',post_view.friend_wall, name = 'friend_wall'),
    path('messages/', messages_view.message_view, name='messages_view'),
    path('create_message/', Message_Create.as_view(), name='message_create'),
    path('chat/<str:username>/',messages_view.chat,name="chat"),

    path('groups/', group_view.group_home, name='group_home'),
    path('create_group/', Group_Create.as_view(), name='group_create'),
    path('update_group/', Group_Update.as_view(), name='group_update'),
    path('create_group_post/', Group_Post_Create.as_view(), name='group_post_create'),
    path('mygroup/<str:group_name>/',group_view.mygroup,name="mygroup"),
    path('create_group_join_request/', Group_Join_request_Create.as_view(), name='group_join_reequest_create'),
    path('add_group_member/<str:group_name>/<int:pk>/',group_view.add_group_member,name="add_group_member"),
    path('remove_group_member/<str:group_name>/<str:username>/',group_view.remove_group_member,name="remove_group_member"),

    path('wallet/', wallet_view.wallet_home, name='wallet_home'),
    path('create_wallet/', Wallet_Create.as_view(), name='wallet_create'),
    path('create_transaction/', Transaction_Create.as_view(), name='transaction_create'),
    path('create_transaction_start/', wallet_view.create_transcation_start, name='transaction_create_start'),
    path('create_add_money_transaction/', Add_Money_Transaction_Create.as_view(), name='add_money_transaction_create'),
    path('accept_transaction/<int:pk>/', wallet_view.accept_transaction, name='accept_transaction'),
    path('view_transaction_logs/', wallet_view.view_transaction_logs, name='view_transaction_logs'),

    # path('fakelogin/',Fakeuser_Login_Create.as_view(),name="fake_login"),
    path('register/',user_view.register,name="register"),
    path('profile/<str:username>/',user_view.profile,name="profile"),
	path('login/', auth_view.LoginView.as_view(template_name='Users/login.html',authentication_form=OTPAuthentication), name='login'),
    path('otpreg/', user_view.otp_show, name='otp-reg'),
	path('logout/', auth_view.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    path('change_password/', auth_view.PasswordChangeView.as_view(success_url=reverse_lazy('change_password_done'),template_name='Users/change_password.html'), name='change_password'),
    path('change_password_done/', auth_view.PasswordChangeDoneView.as_view(template_name='Users/change_password_done.html'), name='change_password_done'),

    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='Users/password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='Users/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),


    path('friends/',user_view.friend_page,name="friend_page"),
    path('friends/add_friend/<int:pk>/',user_view.add_friend,name="add_friend"),
    path('friends/remove_friend/<int:pk>/',user_view.remove_friend,name="remove_friend"),
]
