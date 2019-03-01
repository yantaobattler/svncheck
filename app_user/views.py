from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

usr_list = [
    {'user': 'qwe', 'pwd': '123'},
    {'user': 'asd', 'pwd': '456'}
]


def door(request):
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