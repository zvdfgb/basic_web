from django import forms

class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200,min_length=1,required=True)
    content = forms.CharField(min_length=1,required=False)
    category = forms.IntegerField()
    cover = forms.ImageField(required=False)