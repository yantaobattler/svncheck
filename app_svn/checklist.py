from app_svn.models import check_main
from app_svn.models import check_detail
from django.http import JsonResponse
from app_svn import checkresourcelist
import json


def docheck(request):
    data = json.loads(request.body.decode('utf-8'))
    req_dict = data.get('field')
    check_no = req_dict['check_no']
    path = check_main.objects.get(check_no=check_no).path
    update_check_main(req_dict, check_no)  # 更新主表
    checkresourcelist.docheck(check_no, path)  # 调用检查函数



def update_check_main(req_dict, check_no):
    sub_req_code = req_dict.get('sub_req_code')
    sub_req_name = req_dict.get('sub_req_name')
    UD_FD_code = req_dict.get('UD_FD_code')
    sys_name = req_dict.get('sys_name')
    _recode = check_main.objects.get(check_no=check_no)
    _recode.sub_req_code = sub_req_code
    _recode.sub_req_name = sub_req_name
    _recode.UD_FD_code = UD_FD_code
    _recode.sys_name = sys_name
    _recode.qm = 'system'  # 检查人暂时只有system
    _recode.save()


def get_result(check_no):
    return