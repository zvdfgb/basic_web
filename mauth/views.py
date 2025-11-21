from email.policy import default

from django.shortcuts import render
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import Captcah
# Create your views here.


def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def send_email_captcha(request):
    #?email=xxx的形式访问
    email=request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":'必须传递邮箱！'})
    #生成验证码（取四位阿拉伯数字
    captcah="".join(random.sample(string.digits,4))
    #储存到数据库中
    Captcah.objects.update_or_create(email=email,defaults={'captcha':captcah})
    send_mail("博客注册验证码",message=f"您的注册验证码为：{captcah}",recipient_list=[email],from_email=None)
    return JsonResponse({"code":200,"message":"邮箱验证码发送成功！"})