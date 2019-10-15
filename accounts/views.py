from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # User model form
from django.contrib.auth.forms import AuthenticationForm # 로그인 form
from django.contrib.auth import login as auth_login # 로그인 함수를 불러오기
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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
        print(type(form))
        if form.is_valid():
            # 로그인
            user = form.get_user()
            print(user)
            auth_login(request, user)
            # request에 user의 정보가 담겨있기 때문에 context를 만들 필요 x
            # templates에서도 사용가능 {{ user.username}}
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }

    return render(request, 'accounts/login.html', context)