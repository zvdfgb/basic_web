from django import forms
from django.contrib.auth import get_user_model
from .models import Captcha

User = get_user_model()

class RegisterForm(forms.Form):
    username= forms.CharField(label='Username',max_length=20,min_length=2,error_messages={
        'required':'请输入你的用户名!',
        'max_length':'用户名在2~20之间!',
        'min_length':'用户名在2~20之间!',
    })
    email = forms.EmailField(label='Email',error_messages={
        'required':'请输入邮箱！',
        'invalid':'请输入正确的邮箱！',
    })
    captcha = forms.CharField(label='Captcha',max_length=4,min_length=4,error_messages={
        'required':'请输入验证码！',
        'max_length':'请输入四位验证码！',
        'min_length':'请输入四位验证码！',
    })
    password = forms.CharField(label='Password',max_length=20,min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经注册！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = Captcha.objects.filter(email=email,captcha=captcha).first()
        if not captcha:
            raise forms.ValidationError("验证码与邮箱不匹配！")
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', error_messages={
        'required': '请输入邮箱！',
        'invalid': '请输入正确的邮箱！',
    })
    password = forms.CharField(label='Password', max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)