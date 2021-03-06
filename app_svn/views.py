from app_svn.models import check_main
from app_user.models import useraccount
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import os
import random
import datetime
import json
from app_svn import checklist
from app_svn import getcheckresult
from app_svn import getcheckcountresult
from app_svn import settag


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
def upload_page(request):
    return render(request, 'upload.html')


def check_page(request):
    check_no = request.session.get('check_no', '')
    if check_no:
        excel_name = check_main.objects.get(check_no=check_no).excel_name
    else:
        excel_name = ''
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


def settag_page(request):
    return render(request, 'settag.html')


def settag_action(request):
    # layui的form提交是json需要这么拿数据
    data = json.loads(request.body.decode('utf-8'))
    req_dict = data.get('field')
    req_dict['user'] = request.session['username']
    # print(req_dict)

    msg = settag.settag_action(req_dict)
    return JsonResponse({'rsp_msg': msg})


def check_count_page(request):
    print('check_count_page')
    user_list = []
    user_names = useraccount.objects.all().values_list('name')
    for name in user_names:
        user_list.append(name[0])  # [0]is str, without [0] is tuple
    return render(request, 'check_count.html', {'user_list': user_list})


def check_count_action(request):

    UD_no = request.POST.get('UD_no')
    name = request.POST.get('name')
    startdate = request.POST.get('startdate')
    enddate = request.POST.get('enddate')
    rsp_dict = getcheckcountresult.getresult(UD_no, name, startdate, enddate)
    return JsonResponse(rsp_dict)


def check_count_detail(request):
    print('check_count_detail')
    check_no = request.GET.get('check_no')
    data_list = getcheckresult.getresult(check_no)
    print(data_list)
    return render(request, 'check_count_detail.html', data_list)


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

