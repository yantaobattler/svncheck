from app_user.models import useraccount
from app_user import logincheck
import json


def change(request):
    data = json.loads(request.body.decode('utf-8'))
    req_dict = data.get('field')

    # 取数据库表
    account = request.session.get('username')
    row = useraccount.objects.filter(account=account)
    pwd = row[0].password

    if pwd != logincheck.encodepwd(req_dict.get('old_password')):
        rsp_msg = '旧密码不正确！'
    else:
        new_pwd = req_dict.get('new_password')
        row.update(password=logincheck.encodepwd(new_pwd))
        rsp_msg = '修改成功！'

    return rsp_msg
