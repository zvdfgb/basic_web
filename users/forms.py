from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# 扩展内置注册表单，增加邮箱字段
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 邮箱为必填项

    class Meta:
        model = User  # 使用Django内置User模型
        fields = ['username', 'email', 'password1', 'password2']  # 注册字段

    # 保存用户数据
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # 保存邮箱
        if commit:
            user.save()  # 提交到数据库
        return user