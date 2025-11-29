from email.policy import default

from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import Captcha
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout
# Create your views here.

User = get_user_model()


@require_http_methods(['GET','POST'])
def mlogin(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                #登录
                login(request,user)
                #如果没有点击记住我，则会在浏览器过期后过期
                if not remember:
                    request.session.set_expiry(0)
                #如果点击了，就什么也不做了，默认两周的过期时间
                return redirect('/')
            else:
                print("邮箱或密码错误")
                # form.add_error('email',"邮箱或密码错误")
                # return render(request,'login.html',context={'form':form})
                return redirect(reverse('mauth:login'))
        return None


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

def mlogout(request):
    logout(request)
    return redirect('/')


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

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile


@login_required
def profile_view(request, user_id=None):
    if user_id:
        target_user = get_object_or_404(User, pk=user_id)
        is_own_profile = (request.user == target_user)
    else:
        target_user = request.user
        is_own_profile = True
    
    # Ensure profile exists (for old users)
    if not hasattr(target_user, 'profile'):
        Profile.objects.create(user=target_user)
    
    if request.method == 'POST' and is_own_profile:
        form = ProfileForm(request.POST, request.FILES, instance=target_user.profile)
        if form.is_valid():
            form.save()
            return redirect('mauth:profile')
    else:
        form = ProfileForm(instance=target_user.profile)
    
    return render(request, 'profile.html', {
        'form': form, 
        'is_own_profile': is_own_profile,
        'target_user': target_user
    })


