from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import localtime
from .models import PrivateMessage
User = get_user_model()


# 1. 盲盒首页
@login_required
def index(request):
    return render(request, 'blind_box/index.html')


# 2. 抽签接口 (核心逻辑)
@login_required
def draw(request):
    if request.method == "POST":
        # 获取所有用户，排除当前登录的用户 (id != request.user.id)
        # exclude(is_superuser=True) 是可选的，如果你不想抽到管理员
        candidates = User.objects.exclude(id=request.user.id)

        # 如果系统里只有你一个人
        if not candidates.exists():
            return JsonResponse({
                'code': 404,
                'message': '当前系统只有你一个人，无法匹配哦！请注册一个新账号试试。'
            })

        # 随机选择一个用户
        lucky_user = random.choice(list(candidates))

        # 返回成功信息和目标用户的ID
        return JsonResponse({
            'code': 200,
            'message': '匹配成功！',
            'data': {
                'target_id': lucky_user.id,
                'username': lucky_user.username
            }
        })

    return JsonResponse({'code': 405, 'message': '请求方法错误'})



# ... (保留之前的 index 和 draw 函数) ...

@login_required
def chat(request, target_id):
    target_user = get_object_or_404(User, pk=target_id)
    current_user = request.user

    # 防止自己跟自己聊天
    if target_user == current_user:
        return redirect('blind_box:index')

    # 处理发送消息 (AJAX POST)
    if request.method == "POST":
        content = request.POST.get('content')
        # 简单校验
        if not content or not content.strip():
            return JsonResponse({'code': 400, 'message': '内容不能为空'})

        # 创建消息
        msg = PrivateMessage.objects.create(
            sender=current_user,
            receiver=target_user,
            content=content
        )

        # 返回成功数据给前端
        return JsonResponse({
            'code': 200,
            'data': {
                'content': msg.content,
                'time': localtime(msg.created_at).strftime("%H:%M"),  # 格式化时间
                'sender_id': msg.sender.id
            }
        })

    # GET 请求：获取历史消息
    messages = PrivateMessage.objects.filter(
        (Q(sender=current_user) & Q(receiver=target_user)) |
        (Q(sender=target_user) & Q(receiver=current_user))
    ).order_by('created_at')

    return render(request, 'blind_box/chat.html', {
        'target_user': target_user,
        'messages': messages
    })