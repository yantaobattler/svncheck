from app_user.models import useraccount
import datetime
import hashlib


# 加密
def encodepwd(password):
    # 创建md5对象
    hl = hashlib.md5()

    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(password.encode(encoding='utf-8'))

    return hl.hexdigest()


# 解密
def decodepwd():
    pass


# 验证密码
def check(account, password, ip):
    row = useraccount.objects.filter(account = account)
    if row:  # 用户名存在
        pwd = row[0].password
        pwd_up = encodepwd(password)  # 取密码
        # 登录时间更新
        row.update(lastlogintime=row[0].logintime)
        row.update(logintime=datetime.datetime.now())
        # 登录IP更新
        row.update(lastloginip=row[0].loginip)
        row.update(loginip=ip)

        if pwd == pwd_up:
            return {'code': '00', 'result': row[0]}  # 密码正确
        else:
            return {'code': '02'}  # 用户存在但密码不对
    else:  # 用户名不存在
        return {'code': '01'}



if __name__=='__main__':
    print(encodepwd('1'))