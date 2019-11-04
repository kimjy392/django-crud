from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Article, Comment
from IPython import embed
from .forms import ArticleForm, CommentForm
from django.core.exceptions import PermissionDenied # 에러를 발생하게 한다.(raise)
from django.http import HttpResponseForbidden # 에러 발생 403(return)
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-id')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if not request.user.is_authenticated:
        return redirect('articles:index')
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
            article.user = request.user
            article.image = request.FILES.get('image')
            article.save()
            # 해시태그 저장 및 연결 작업
            return redirect('articles:detail', article.pk)

    else:
        # GET 요청 -> Form
        article_form = ArticleForm()
        article_form.user = request.user
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
    

@require_POST
def delete(request, article_pk):
    # 작성자와 사용자가 같다면
    if article.user == request.user:
        article = get_object_or_404(Article, pk=article_pk)
        article.delete()
        return redirect('articles:index')
    else:
        # 다르다면 에러
        raise PermissionDenied


@login_required
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

@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
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
            comment.user = request.user
            comment.save()
            messages.info(request, '댓글이 생성되었습니다.')
        else:
            messages.success(request, '댓글 형식이 맞지 않습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponse('Unauthorized', article_pk)
    # comment = Comment.objects.create(content=request.POST.get('content'), article_id=article_pk)
 

@require_POST
def comment_delete(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        article_pk = comment.article.pk
        comment.delete()
        messages.info(request, '댓글이 삭제되었습니다.')
        return redirect('articles:detail', article_pk)
    else:
        return HttpResponseForbidden('이렇게 들어오려고 하지마')

# request.user를 사용하려면 @login_required 나 authenticated을 사용해서 로그인이 되어있는지 확인해야한다!(로그인이 안되어 있을 경우도 생각해서 request.user는 )
@login_required
def like(request, article_pk):
    if request.is_ajax():
        article = Article.objects.get(pk=article_pk)
        # 좋아요를 누른적이 있다면
        if request.user in article.like_users.all():
            # 좋아요 취소 로직
            article.like_users.remove(request.user)
            is_liked = False
        # 아니면
        else:
            # 좋아요 로직
            request.user.like_articles.add(article)
            is_liked = True
        return JsonResponse({'is_liked' : is_liked, 'like_users':article.like_users.count()})
    else:
        HttpResponseForbidden()