from django.urls import path
from . import views


app_name = 'mauth'

urlpatterns = [
    path('login',views.mlogin,name='login'),
    path('register',views.register,name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
    path('logout',views.mlogout,name='logout'),
]