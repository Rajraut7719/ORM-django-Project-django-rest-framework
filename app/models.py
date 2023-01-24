from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class STATUS(models.TextChoices):
    DRAFT = "0",("DRAFT")
    PUBLISH = "1",('PUBLISH')
    ARCHIVE = "2",("ARCHIVE")


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    description = models.TextField(max_length=250,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.title}"
        
class Post(models.Model):
    author = models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    summary = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField()
    status = models.CharField(max_length=1,choices=STATUS.choices,default=STATUS.DRAFT)
    image = models.ImageField(upload_to="post",default='post/sample.jpg')
    category = models.ManyToManyField(Category,related_name='posts')
    views = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"User ->{self.author.username} Title ->{self.title} Views -> {self.views}"

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    text= models.TextField()
    approved_comment = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"username ->{self.author.username} post -> {self.post.title},comment ->{self.text}"

class Like(models.Model):
    user = models.ForeignKey(User,related_name='likes',on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='likes',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.post.title}  -> {self.user.username}"
