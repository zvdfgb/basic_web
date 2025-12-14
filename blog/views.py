from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from blog.models import BlogCategory,Blog,BlogComment,BlogTag
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
            tags_str = form.cleaned_data.get('tags', '').strip()
            
            print(f"DEBUG: Received tags_str: '{tags_str}'")
            print(f"DEBUG: Raw POST tags: '{request.POST.get('tags')}'")

            blog = Blog.objects.create(title=title,content=content,category_id=category_id,author=request.user)
            if cover:
                 blog.cover = cover
                 blog.save()
            
            if tags_str:
                tag_names = [name.strip() for name in tags_str.replace('，', ',').split(',') if name.strip()]
                print(f"DEBUG: Parsed tag_names: {tag_names}")
                for name in tag_names:
                    tag, created = BlogTag.objects.get_or_create(name=name)
                    blog.tags.add(tag)
                    print(f"DEBUG: Added tag: {name} (Created: {created})")

            return JsonResponse({'code':200,"message":"博客发布成功","data":{"blog_id":blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code':400,"message":"参数错误！"})


@require_POST
def pub_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'code': 401, 'message': '请先登录！'})

    print("DEBUG: pub_comment view reached!")
    print(f"DEBUG: User: {request.user}")
    print(f"DEBUG: POST data: {request.POST}")
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
         html = render_to_string('components/comment_reply.html', context, request=request)
    else:
         # It's a root comment
         # Need to pass 'blog' in context if needed, though simpler template avoids it
         context['blog'] = new_comment.blog 
         html = render_to_string('components/comment_root.html', context, request=request)
         
    return JsonResponse({'code': 200, 'message': '评论成功', 'html': html, 'parent_id': parent_id})


@require_GET
def search(request):
    q = request.GET.get('q', '')
    if q:
        # Filter blogs by title or content matching the query
        blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)).distinct().order_by('-pub_time')
    else:
        # If no query provided, return an empty list (or could redirect to index)
        blogs = []
    
    return render(request, 'search_results.html', context={'blogs': blogs, 'query': q})


@require_POST
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user != blog.author and not request.user.is_superuser:
        return JsonResponse({'code': 403, 'message': 'Permission denied'})
    
    blog.delete()
    return JsonResponse({'code': 200, 'message': 'Blog deleted successfully'})

@require_POST
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(BlogComment, pk=comment_id)
    if request.user != comment.author and not request.user.is_superuser:
        return JsonResponse({'code': 403, 'message': 'Permission denied'})
    
    comment.delete()
    return JsonResponse({'code': 200, 'message': 'Comment deleted successfully'})



@require_POST
@login_required
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    try:
        comment = BlogComment.objects.get(pk=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            is_liked = False
        else:
            comment.likes.add(request.user)
            is_liked = True
        
        return JsonResponse({
            'code': 200, 
            'message': 'Success', 
            'data': {
                'is_liked': is_liked,
                'likes_count': comment.likes.count()
            }
        })
    except BlogComment.DoesNotExist:
        return JsonResponse({'code': 404, 'message': 'Comment not found'})
