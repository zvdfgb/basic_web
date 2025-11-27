from django.urls import path
from . import views

app_name = 'blind_box'

urlpatterns = [
    path('', views.index, name='index'),           # 盲盒首页
    path('draw/', views.draw, name='draw'),        # 抽奖动作
    path('chat/<int:target_id>/', views.chat, name='chat'), # 聊天页
]