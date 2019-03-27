from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def check(request):
    return render(request, 'check.html')


def settag(request):
    return render(request, 'settag.html')


def check_count(request):
    return render(request, 'check_count.html')


def upload(request):
    file_obj = request.FILES.get('file')
    path = os.path.join(BASE_DIR, 'tempfiles', file_obj.name)
    request.session["uploadpath"] = path
    f = open(path, 'wb')
    print(file_obj, type(file_obj))
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    print('11111')
    return JsonResponse({'rsp_msg': 'success'})
