from django.urls import path
from . import views

app_name = 'mauth'

urlpatterns = [
    path('login',views.mlogin,name='login'),
    path('register',views.register,name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
    path('logout',views.mlogout,name='logout'),
    path('profile', views.profile_view, name='profile'),

    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('friend/add/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend/accept/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend/reject/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friends/', views.friend_list, name='friend_list'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('chat/get_messages/<int:user_id>/', views.get_messages, name='get_messages'),
]