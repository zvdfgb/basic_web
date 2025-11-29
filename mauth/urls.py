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
]