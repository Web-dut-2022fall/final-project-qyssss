from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm

# 文章评论


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id):
    article = ArticlePost.objects.get(id=article_id)
    # 处理POST
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("输入有误,请重试")
    # 处理错误请求
    else:
        return HttpResponse("发表评论使用POST")
