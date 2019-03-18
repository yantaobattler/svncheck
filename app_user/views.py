from django.shortcuts import render
from django.shortcuts import HttpResponse
from app_user import *
# Create your views here.

usr_list = [
    {'user': 'qwe', 'pwd': '123'},
    {'user': 'asd', 'pwd': '456'}
]


def login(request):
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


def main(request):
    print('cmdb')
    # return HttpResponse('hello world!')
    # 必须大写POST
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(username, password)
        tmp = {'user': username, 'pwd': password}
        usr_list.append(tmp)
    return render(request, 'index.html', {'data':usr_list})