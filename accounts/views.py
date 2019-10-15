from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # User model form
from django.contrib.auth.forms import AuthenticationForm # 로그인 form
from django.contrib.auth import login as auth_login # 로그인 함수를 불러오기
from django.contrib.auth import logout as auth_logout # 로그아웃 함수 불러오기
from IPython import embed
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # 회원가입하고 바로 로그인이 되어있다.
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
        
    else:
        form = UserCreationForm()
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