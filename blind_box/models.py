from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model

# 获取当前项目使用的用户模型
User = get_user_model()

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_msgs', on_delete=models.CASCADE, verbose_name="发送者")
    receiver = models.ForeignKey(User, related_name='received_msgs', on_delete=models.CASCADE, verbose_name="接收者")
    content = models.TextField(verbose_name="消息内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        ordering = ['created_at'] # 保证聊天记录按时间顺序显示
        verbose_name = "私信"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:10]}"