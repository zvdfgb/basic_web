from django.shortcuts import render,reverse,redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST
from blog.models import BlogCategory,Blog,BlogComment
from .forms import PubBlogForm

# Create your views here.

def index(request):
    return render(request, 'index.html')




def blog_detail(request,blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, 'blog_detail.html',context={'blog':blog,blog_id:'blog_id'})





@login_required()
@require_http_methods(["GET","POST"])
def pub_blog(request):
    if request.method == "GET":
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html',context={'categories':categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            blog = Blog.objects.create(title=title,content=content,category_id=category_id,author=request.user)
            return JsonResponse({'code':200,"message":"博客发布成功","data":{"blog_id":blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code':400,"message":"参数错误！"})


@require_POST
@login_required()
def pub_comment(request):
    blog_id =  request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id,content=content,author=request.user)
    #重新加载博客详情页
    return redirect(reverse("blog:blog_detail",kwargs={"blog_id":blog_id}))