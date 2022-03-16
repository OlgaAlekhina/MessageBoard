from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=250)
    post_text = HTMLField()

    def __str__(self):
        return f'{self.post_title}'

    def get_absolute_url(self):
        return f'/main/{self.id}'

    def comments_number(self):
        comments = Reply.objects.filter(reply_post=self, reply_approved=True)
        number = len(comments)
        return number


class Reply(models.Model):
    reply_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    reply_time = models.DateTimeField(auto_now_add=True)
    reply_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reply_text}'

