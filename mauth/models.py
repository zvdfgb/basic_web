from django.db import models


# Create your models here.


class Captcha(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now_add=True)


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True, verbose_name='个性签名')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('S', '保密'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='S', verbose_name='性别')
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='地区')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    is_public = models.BooleanField(default=True, verbose_name='是否公开个人主页')


    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']