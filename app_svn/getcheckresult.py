from app_svn.models import check_detail
from app_svn import tools


def getresult(check_no):
    rsp_dict = {"code": 0, "msg": ""}
    query = check_detail.objects.filter(check_no=check_no).order_by('id')
    rsp_dict['count'] = query.count()
    data_list = []
    if rsp_dict['count'] == 0:
        data = {}
        data['check_no'] = '无问题'  # 流水号
        data['excel_line'] = '无问题'  # 行数
        data['line_name'] = '无问题'  # 文件名
        data['problem'] = '无问题'  # 取错误编号对应的中文名
        data_list.append(data)
    else:
        for each_line in query:
            data = {}
            data['check_no'] = each_line.check_no  # 流水号
            data['excel_line'] = each_line.excel_line  # 行数
            if each_line.line_name == 'head':  # 文件名
                data['line_name'] = '表头'
            else:
                data['line_name'] = each_line.line_name
            data['problem'] = tools.problem_dict.get(each_line.problem)  # 取错误编号对应的中文
            data_list.append(data)
    rsp_dict['data'] = data_list
    return rsp_dict