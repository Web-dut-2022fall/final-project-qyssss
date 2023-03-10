from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    # 评论后路由重定向

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
