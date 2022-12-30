from django.contrib.auth.models import User

from comment.models import Comment
from .forms import ArticlePostForm
from django.shortcuts import render, redirect
import markdown
from django.http import HttpResponse
from .models import ArticlePost
from django.core.paginator import Paginator
from django.db.models import Q

# 文章列表(实现分页)


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 搜索文章
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 分页功能
    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 增加 search 到 context
    context = {'articles': articles, 'order': order, 'search': search}

    return render(request, 'article/list.html', context)


# 文章详情

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 用户访问就浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                     ])

    # 添加comments上下文
    context = {'article': article, 'comments': comments}
    return render(request, 'article/detail.html', context)

# 创建新文章


def article_create(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)

# 删文章


def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

# 修改文章


def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)
