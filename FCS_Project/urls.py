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
from django.urls import path,include
from Users import views as user_view
from django.contrib.auth import views as auth_view
from Messages import views as messages_view
from Groups import views as group_view
from Wallet import views as wallet_view
from Messages.views import Message_Create
from Groups.views import Group_Create,Group_Post_Create,Group_Join_request_Create
from Wallet.views import Wallet_Create,Transaction_Create,Add_Money_Transaction_Create

urlpatterns = [
	path('admin/', admin.site.urls),
	path('Wall/', include('Wall.urls')),
    
    path('messages/', messages_view.message_view, name='messages_view'),
    path('create_message/', Message_Create.as_view(), name='message_create'),
    path('chat/(?P<username>.+)/',messages_view.chat,name="chat"),

    path('groups/', group_view.group_home, name='group_home'),
    path('create_group/', Group_Create.as_view(), name='group_create'),
    path('create_group_post/', Group_Post_Create.as_view(), name='group_post_create'),
    path('mygroup/(?P<group_name>.+)/',group_view.mygroup,name="mygroup"),
    path('create_group_join_request/', Group_Join_request_Create.as_view(), name='group_join_reequest_create'),
    path('add_group_member/(?P<group_name>.+)/(?P<pk>\d+)/',group_view.add_group_member,name="add_group_member"),
    path('remove_group_member/(?P<group_name>.+)/(?P<pk>\d+)/',group_view.remove_group_member,name="remove_group_member"),

    path('wallet/', wallet_view.wallet_home, name='wallet_home'),
    path('create_wallet/', Wallet_Create.as_view(), name='wallet_create'),
    path('create_transaction/', Transaction_Create.as_view(), name='transaction_create'),
    path('create_add_money_transaction/', Add_Money_Transaction_Create.as_view(), name='add_money_transaction_create'),
    path('accept_transaction/(?P<pk>\d+)/', wallet_view.accept_transaction, name='accept_transaction'),

    path('register/',user_view.register,name="register"),
    path('profile/(?P<username>.+)/',user_view.profile,name="profile"),
	path('login/', auth_view.LoginView.as_view(template_name='Users/login.html'), name='login'),
	path('logout/', auth_view.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    
    path('friends/',user_view.friend_page,name="friend_page"),
    path('friends/add_friend/(?P<pk>\d+)/',user_view.add_friend,name="add_friend"),
    path('friends/remove_friend/(?P<pk>\d+)/',user_view.remove_friend,name="remove_friend"),
]
