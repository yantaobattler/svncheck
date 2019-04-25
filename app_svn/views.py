from app_svn.models import check_main
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import os
import random
import datetime
import json
from app_svn import checklist
from app_svn import getcheckresult


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def upload_page(request):
    return render(request, 'upload.html')


def check_page(request):
    check_no = request.session['check_no']
    excel_name = check_main.objects.get(check_no=check_no).excel_name
    return render(request, 'check.html', {'check_no': check_no, 'excel_name': excel_name})


def check_result_page(request):
    return render(request, 'check_result.html')


def check_result_action(request):
    check_no = request.session['check_no']
    rsp_list = getcheckresult.getresult(check_no)
    message_json = json.dumps(rsp_list)
    return HttpResponse(message_json)  # 请求是get，得这么回


def check_action(request):
    checklist.docheck(request)
    return JsonResponse({'rsp_msg': '1'})

def settag(request):
    return render(request, 'settag.html')


def check_count(request):
    return render(request, 'check_count.html')


def upload(request):
    file_obj = request.FILES.get('file')
    check_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100000,999999))
    path = os.path.join(BASE_DIR, 'tempfiles', file_obj.name)
    request.session["check_no"] = check_no  # 本次检查流水号
    request.session["file_name"] = file_obj.name  # excel文件名
    upload_user = request.session['username']
    # 文件上传
    f = open(path, 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()

    # 写主表
    result = check_main.objects.get_or_create(check_no=check_no,
                                              path=path,
                                              upload_user=upload_user,
                                              excel_name=file_obj.name)
    if result[1]:
        msg = '上传成功'
    else:
        msg = '上传失败，请重新上传'
    return JsonResponse({'rsp_msg': msg})

