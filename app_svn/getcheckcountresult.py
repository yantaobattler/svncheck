from app_svn.models import check_detail
from app_svn.models import check_main
from app_user.models import useraccount
import datetime


def getresult(UD_no, name, startdate, enddate):
    rsp_dict = {"code": 0, "msg": ""}

    # 截止日期为下一日0点
    enddate_date = datetime.datetime.strptime(enddate, "%Y-%m-%d")
    enddate_date += datetime.timedelta(days=1)
    enddate = enddate_date.strftime("%Y-%m-%d")

    detail_query = check_main.objects.filter(upload_time__gte=startdate, upload_time__lte=enddate).order_by('id')
    if UD_no:
        detail_query = detail_query.filter(UD_FD_code=UD_no)
    if name:
        user = useraccount.objects.get(name=name).account
        detail_query = detail_query.filter(upload_user=user)
    rsp_dict['count'] = detail_query.count()
    data_list = []
    if rsp_dict['count'] == 0:
        data = {}
        data['check_no'] = '无数据'  # 流水号
        data['UD_FD_code'] = ''  # 投产编号
        data['sub_req_code'] = ''  # 子需求编号
        data['sub_req_name'] = ''  # 子需求名
        data['upload_user'] = ''  # 提交用户
        data['problem_count'] = ''  # 问题数
        data['upload_time'] = ''  # 提交日期
        data_list.append(data)
    else:
        for each_line in detail_query:
            data = {}
            data['check_no'] = each_line.check_no  # 流水号
            data['UD_FD_code'] = each_line.UD_FD_code  # 投产编号
            data['sub_req_code'] = each_line.sub_req_code  # 子需求编号
            data['sub_req_name'] = each_line.sub_req_name  # 子需求名
            data['upload_user'] = each_line.upload_user  # 提交用户
            data['upload_time'] = str(each_line.upload_time)[:19]  # 提交日期

            check_no = each_line.check_no
            problem_count = check_detail.objects.filter(check_no=check_no).count()
            data['problem_count'] = problem_count  # 问题数
            data_list.append(data)

    rsp_dict['data'] = data_list
    return rsp_dict


