from email.policy import default

from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import Captcha
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

def login(request):
    return render(request,'login.html')

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email,username=username,password=password)
            return redirect(reverse('mauth:login'))
        else:
            print(form.errors)
            #重新跳转到注册页面
            return redirect(reverse('mauth:register'))
            # return render(request,'register.html',context={'form':form})

def send_email_captcha(request):
    #?email=xxx的形式访问
    email=request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":'必须传递邮箱！'})
    #生成验证码（取四位阿拉伯数字
    captcah="".join(random.sample(string.digits,4))
    #储存到数据库中
    Captcha.objects.update_or_create(email=email,defaults={'captcha':captcah}  )
    send_mail("博客注册验证码",message=f"您的注册验证码为：{captcah}",recipient_list=[email],from_email=None)
    return JsonResponse({"code":200,"message":"邮箱验证码发送成功！"})