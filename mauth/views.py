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
    
    are_friends = False
    sent_request_pending = False
    received_request_pending = False  # Initialize it here
    received_request_id = None
    if not is_own_profile:
        # Check if they are already friends
        are_friends = request.user.profile.friends.filter(user=target_user).exists()
        
        # Check if a request has been sent by current user to target user
        sent_request_pending = FriendRequest.objects.filter(
            from_user=request.user, to_user=target_user, status='pending'
        ).exists()

        # Check if a request has been sent by target user to current user
        received_request = FriendRequest.objects.filter(
            from_user=target_user, to_user=request.user, status='pending'
        ).first()
        if received_request:
            received_request_pending = True
            received_request_id = received_request.id

    # Visibility Check
    if not is_own_profile and not target_user.profile.is_public:
        # If not public, allow only friends
        if not are_friends:
             return render(request, 'profile_private.html', {'target_user': target_user})

    if request.method == 'POST' and is_own_profile:
        form = ProfileForm(request.POST, request.FILES, instance=target_user.profile)
        if form.is_valid():
            form.save()
            return redirect('mauth:profile')
    else:
        form = ProfileForm(instance=target_user.profile)
    
    blogs = target_user.blog_set.all().order_by('-pub_time')

    return render(request, 'profile.html', {
        'form': form, 
        'is_own_profile': is_own_profile,
        'target_user': target_user,
        'blogs': blogs,
        'are_friends': are_friends,
        'sent_request_pending': sent_request_pending,
        'received_request_pending': received_request_pending,
        'received_request_id': received_request_id,
    })


from .models import FriendRequest, Message
from django.db.models import Q

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)
    if request.user == to_user:
        return JsonResponse({'status': 'error', 'message': 'Cannot send request to yourself'})
    
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return JsonResponse({'status': 'error', 'message': 'Request already sent'})
    
    if request.user.profile.friends.filter(pk=user_id).exists():
        return JsonResponse({'status': 'error', 'message': 'Already friends'})

    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return JsonResponse({'status': 'success', 'message': 'Friend request sent'})

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)
    if friend_request.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Request already processed'})
    
    friend_request.status = 'accepted'
    friend_request.save()
    
    # Add to friends list for both users
    request.user.profile.friends.add(friend_request.from_user.profile)
    friend_request.from_user.profile.friends.add(request.user.profile)
    
    return JsonResponse({'status': 'success', 'message': 'Friend request accepted'})

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, pk=request_id, to_user=request.user)
    if friend_request.status != 'pending':
        return JsonResponse({'status': 'error', 'message': 'Request already processed'})
    
    friend_request.status = 'rejected'
    friend_request.save()
    return JsonResponse({'status': 'success', 'message': 'Friend request rejected'})

@login_required
def friend_list(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    friends = request.user.profile.friends.all()
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    
    # Get all users except self and already friends
    # We need to filter out users who are already friends
    friend_users = [f.user.id for f in friends]
    all_users = User.objects.exclude(pk=request.user.pk).exclude(pk__in=friend_users)
    
    recommended_user = None
    if not friends.exists() and all_users.exists():
        count = all_users.count()
        if count > 0:
            random_index = random.randint(0, count - 1)
            recommended_user = all_users[random_index]
    
    return render(request, 'mauth/friend_list.html', {
        'friends': friends,
        'received_requests': received_requests,
        'sent_requests': sent_requests,
        'all_users': all_users,
        'recommended_user': recommended_user
    })


@login_required
def chat_view(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    # Check if they are friends
    if not request.user.profile.friends.filter(user=friend).exists():
        return redirect('mauth:friend_list')
        
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=friend, content=content)
            return JsonResponse({'status': 'success'})
            
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=friend) | 
        Q(sender=friend, receiver=request.user)
    ).order_by('timestamp')
    
    # Get all friends for the sidebar
    friends = request.user.profile.friends.all()
    
    return render(request, 'mauth/chat.html', {
        'friend': friend,
        'messages': messages,
        'friends': friends  # Added friends list
    })

@login_required
def get_messages(request, user_id):
    friend = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=friend) | 
        Q(sender=friend, receiver=request.user)
    ).order_by('timestamp')
    
    # Mark received messages as read
    Message.objects.filter(sender=friend, receiver=request.user, is_read=False).update(is_read=True)
    
    messages_data = [{
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_self': msg.sender == request.user
    } for msg in messages]
    
    return JsonResponse({'messages': messages_data})



