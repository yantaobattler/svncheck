from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from app_user import *
from app_svn import *

# Create your views here.

usr_list = [
    {'user': 'qwe', 'pwd': '123'},
    {'user': 'asd', 'pwd': '456'}
]


def login(request):
    request.session.delete(request.session.session_key)
    if request.method == 'POST':
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
    elif request.method == 'GET':
        account = request.GET.get('account', None)
        password = request.GET.get('password', None)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

    if account and password:
        checkresult = logincheck.check(account, password, ip)
        if checkresult.get('code') == '00':  # 正常
            request.session["username"] = account
            return render(request, 'index.html', {'data': checkresult.get('result')})
        elif checkresult.get('code') == '01':  # 用户名不存在
            msg = '用户名不存在'
            return render(request, 'login.html', {'msg': msg})
        elif checkresult.get('code') == '02':  # 密码不正确
            msg = '密码不正确'
            return render(request, 'login.html', {'msg': msg})
    return render(request, 'login.html')


def mainblank(request):
    return render(request, 'mainblank.html')


def index(request):
    return render(request, 'index.html')


def chg_pwd(request):
    return render(request, 'change_pwd.html')


def chgpwd_action(request):
    rsp_msg = chgpwd.change(request)
    return JsonResponse({'rsp_msg': rsp_msg})

