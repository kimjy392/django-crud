from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Article, Comment
from IPython import embed
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    embed()
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def create(request):
    if request.method == 'POST':
        # POST 요청 -> 검증 및 저장
        # 저장 로직
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        article_form = ArticleForm(request.POST, request.FILES)
        # 검증에 성공하면 저장하고
        if article_form.is_valid():
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()
            article = article_form.save(commit=False)
            article.image = request.FILES.get('image')
            article.save()
            return redirect('articles:detail', article.pk)
    
    else:
        # GET 요청 -> Form
        article_form = ArticleForm()
        # GET - > 비어있는 Form  context
        # POST -> 검증 실패시 에러메세지와 입력값 채워진 Form context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form' : comment_form
    }
    return render(request, 'articles/detail.html', context)

from django.views.decorators.http import require_POST
@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article = article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article = Article.objects.get(pk=article_pk)
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 1. modelform에 사용자 입력값 넣고
    comment_form = CommentForm(request.POST)
    # 2. 검증하고,
    if comment_form.is_valid():
    # 3. 맞으면 저장,
        # 3-1. 사용자 입력값으로 comment instance 생성(저장은 X)
        comment = comment_form.save(commit=False)
        # 3-2. FK 넣고 저장
        comment.article = article
        comment.save()
        messages.info(request, '댓글이 생성되었습니다.')
    else:
        messages.success(request, '댓글 형식이 맞지 않습니다.')
    return redirect('articles:detail', article_pk)
    # comment = Comment.objects.create(content=request.POST.get('content'), article_id=article_pk)
 

def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article_pk = comment.article.pk
    comment.delete()
    messages.info(request, '댓글이 삭제되었습니다.')
    return redirect('articles:detail', article_pk)