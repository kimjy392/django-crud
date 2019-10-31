from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # User model form
from django.contrib.auth.forms import AuthenticationForm # 로그인 form
from django.contrib.auth.forms import PasswordChangeForm # password change form
from django.contrib.auth import update_session_auth_hash # session을 update하는데 지금가지는 hash값으로
from django.contrib.auth import login as auth_login # 로그인 함수를 불러오기
from django.contrib.auth import logout as auth_logout # 로그아웃 함수 불러오기
from django.contrib.auth.decorators import login_required # 로그인이 요구되어질때
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from IPython import embed

from .forms import CustomUserChangeForm
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # 회원가입하고 바로 로그인이 되어있다.
            user = form.save()
            print(type(user))
            embed()
            auth_login(request, user)
            return redirect('articles:index')
        
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        # request에는 모든 정보가 다 담겨있기 때문에 쿠키나 세션등...
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인
            user = form.get_user()
            auth_login(request, user)
            # request에 user의 정보가 담겨있기 때문에 context를 만들 필요 x
            # templates에서도 사용가능 {{ user.username}}
            # request.GET.get('next') : 없으면 none를 반환, 있으면 next이후의 url를 가지고 있다.
            print(request.GET.get('next'))
            return redirect(request.GET.get('next') or 'articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    # request.user.is_authenticated 는 로그인이 되어있냐 아니냐를 boolean
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        # 1. 사용자가 보낸 내용 담아서
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 2. 검증
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 비밀번호가 달라졌기 때문에 세션 정보가 달라져서 로그인이 풀린다.
            # 다음 함수로 로그인을 유지한다.
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/update.html', context)

def profile(request, account_pk):
    # user = User.objects.get(pk=account_pk)
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk)
    context = {
        'user_profile' : user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User, pk=account_pk)
    if request.user != obama:
        # obama을 팔로우 한적 있다면
        if request.user in obama.followers.all():
            # 취소
            obama.followers.remove(request.user)
        else:
            obama.followers.add(request.user)
    return redirect('accounts:profile', account_pk)
    