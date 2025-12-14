from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.index,name='index'),
    path('blog/detail/<int:blog_id>',views.blog_detail,name='blog_detail'),
    path('blog/pub',views.pub_blog,name='blog_pub'),
    path('blog/commment/pub',views.pub_comment,name='pub_comment'),
    path('comment/like', views.like_comment, name='like_comment'),
    path('blog/delete/<int:blog_id>',views.delete_blog,name='delete_blog'),
    path('comment/delete/<int:comment_id>',views.delete_comment,name='delete_comment'),
    path('search',views.search,name='search'),
]