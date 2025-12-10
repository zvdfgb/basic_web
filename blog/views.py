from django.shortcuts import render,reverse,redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from blog.models import BlogCategory,Blog,BlogComment
from .forms import PubBlogForm
from django.db.models import Q

# Create your views here.

def index(request):
    blogs = Blog.objects.all().order_by('-pub_time')
    return render(request, 'index.html', context={'blogs': blogs})




def blog_detail(request,blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    
    # Fetch only root comments (those without a parent)
    comments = BlogComment.objects.filter(blog=blog, parent=None).order_by('-pub_time')
    
    return render(request, 'blog_detail.html',context={'blog':blog,'blog_id':blog_id, 'comments': comments})


@login_required()
@require_http_methods(["GET","POST"])
def pub_blog(request):
    if request.method == "GET":
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html',context={'categories':categories})
    else:
        form = PubBlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_id = form.cleaned_data['category']
            cover = form.cleaned_data.get('cover')
            blog = Blog.objects.create(title=title,content=content,category_id=category_id,author=request.user)
            if cover:
                 blog.cover = cover
                 blog.save()
            return JsonResponse({'code':200,"message":"博客发布成功","data":{"blog_id":blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code':400,"message":"参数错误！"})


@require_POST
@login_required()
def pub_comment(request):
    blog_id =  request.POST.get('blog_id')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')
    
    parent_comment = None
    if parent_id:
        try:
            parent_comment = BlogComment.objects.get(id=parent_id)
        except BlogComment.DoesNotExist:
            pass

    new_comment = BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user, parent=parent_comment)
    
    # Reload the new comment object to ensure relations are accessible for template
    new_comment.refresh_from_db()
    
    # Render the comment HTML
    from django.template.loader import render_to_string
    context = {'comment': new_comment}
    if new_comment.parent:
         # It's a reply
         html = render_to_string('components/comment_reply.html', context)
    else:
         # It's a root comment
         # Need to pass 'blog' in context if needed, though simpler template avoids it
         context['blog'] = new_comment.blog 
         html = render_to_string('components/comment_root.html', context)
         
    return JsonResponse({'code': 200, 'message': '评论成功', 'html': html, 'parent_id': parent_id})


@require_GET
def search(request):
    q = request.GET.get('q', '')
    if q:
        # Filter blogs by title or content matching the query
        blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-pub_time')
    else:
        # If no query provided, return an empty list (or could redirect to index)
        blogs = []
    
    return render(request, 'search_results.html', context={'blogs': blogs, 'query': q})
