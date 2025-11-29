from django import forms
from .models import Profile

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确的邮箱'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请传入用户名',
        'max_length': '用户名长度在2-20之间',
        'min_length': '用户名长度在2-20之间'
    })
    email = forms.EmailField(error_messages={'required': '请传入邮箱', 'invalid': '请传入正确的邮箱'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='邮箱', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'nickname', 'signature', 'age', 'gender', 'region']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'signature': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            user = profile.user
            user.email = self.cleaned_data['email']
            user.save()
        return profile