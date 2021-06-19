from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfileInfo(models.Model):
    id = models.IntegerField(primary_key=True,default=1)
    user = models.OneToOneField(User,on_delete=CASCADE)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    bio = models.CharField(max_length=1000,blank=True)
    picture = models.ImageField(upload_to ='profile_pics/',blank=True)

    def __str__(self):
        return(self.user.username)

    def get_absolute_url(self):
        return(reverse('my_profile', kwargs={'pk': self.pk}))


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=CASCADE,related_name='posts')
    title = models.CharField(max_length=200)
    support_content = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True)

    def get_absolute_url(self):
        return(reverse('post_detail', kwargs={'pk': self.pk}))

    def approved_comments(self):
        return(self.comments.filter(create_date__lte=timezone.now()).order_by('-create_date'))

    def __str__(self):
        return(self.title)

    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post,related_name='comments',on_delete=CASCADE)
    author = models.CharField(max_length=264,blank=True)
    text = models.TextField()
    create_date = models.DateTimeField(blank=True)

    def get_absolute_url(self):
        return(reverse('blog:post_list'))

    def __str__(self):
        return(self.text)
    