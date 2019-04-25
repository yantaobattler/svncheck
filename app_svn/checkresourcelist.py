# -*-coding:utf-8-*-
# !/usr/bin/env Python
# coding=utf-8

'''''''''''''''''''''''''''''''''''''''''''''
##天津农商银行 源码清单检查工具
##闫涛@应用开发中心
##
##91请删除无用sheet页
##92建议项目名称填需求编号+需求名
##93请填写项目名称
##94请检查上线编号
##95请填写上线编号
##01请删除空行
##02注意斜杠格式应该为/
##03路径应该以https开头
##04该路径源码无此版本源码
##05源码清单登记非最新版本源码请确认
##06源码上传说明建议以软件需求编号开头
##07开发人员应于svn上传人用户名相同
##08提交日期与SVN服务器应一致
##09源码清单不应包含文件夹记录
##10版本号不可为空
##11提交日期不可为空
##12开发人员不可为空
##13版本号须为数值型
##14日期须为日期型
'''''''''''''''''''''''''''''''''''''''''''''
import svn
import time
import openpyxl
from app_svn import tools
from app_svn.models import check_detail

authorpath = ''
write_file = ''
action = ''
result = ''
checking_temp = []


# 取SVN用户表查询中文名对应的英文用户名
# def checkauthor(name, author_ws):
#     author_list = []
#     author_ws_rows_len = len(list(author_ws.rows))
#     # 读每行
#     for row in range(3, author_ws_rows_len + 1):
#         if author_ws.cell(row=row, column=2).value and name == author_ws.cell(row=row, column=2).value.strip():
#             author_list.append(author_ws.cell(row=row, column=8).value.strip())
#             ##    print(name,'    ',author_list)
#
#     # 返回中文姓名对应的英文用户名list
#     return author_list


# 检查函数
def docheck(check_no, path):
    localpath = path
    # 打开检查文件
    wb = openpyxl.load_workbook(localpath)
    sheets = wb.get_sheet_names()

    # 检查每个sheet
    for sheetnum in range(len(sheets)):
        ws = wb.get_sheet_by_name(sheets[sheetnum])

        # 表头检查

        # 判断该sheet如果有源码则B3应为'程序源码清单'
        if ws['B1'].value or not ws['B3'].value or not '程序源码清单' == ws['B3'].value.strip():
            check_detail.objects.create(check_no=check_no, excel_line=3, line_name='head', problem='91')

            # 检查项目名称
        if ws['C5'].value:
            project_name = ws['C5'].value.strip()
            if not project_name[0:8].isdigit():
                check_detail.objects.create(check_no=check_no, excel_line=5, line_name='head', problem='92')
        else:
            check_detail.objects.create(check_no=check_no, excel_line=5, line_name='head', problem='93')

        # 检查上线编号
        if ws['C7'].value:
            update_no = ws['C7'].value.strip()
            if not (update_no[0:5] == 'UD-20' or update_no[0:5] == 'FD-20'):
                check_detail.objects.create(check_no=check_no, excel_line=7, line_name='head', problem='94')
        else:
            check_detail.objects.create(check_no=check_no, excel_line=7, line_name='head', problem='95')

        # 清单内容检查

        ws_rows_len = len(list(ws.rows))  # 行数
        ws_columns_len = len(list(ws.columns))  # 列数

        # 循环读取每行明细
        for row in range(13, ws_rows_len + 1):
            passed = True
            # 判断该行是否为空
            if not ws.cell(row=row, column=2).value:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name='', problem='01')
                continue  # 该行为空直接下一行

            checking_name = ws.cell(row=row, column=2).value.strip()  # 源码名称
            checking_path = ws.cell(row=row, column=3).value.strip()  # 源码路径

            # 版本号是否为空
            if ws.cell(row=row, column=5).value:
                checking_revision = ws.cell(row=row, column=5).value
            else:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='10')
                passed = False

            # 版本号应该是数值型
            if str(checking_revision).isdigit():
                pass
            else:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='13')
                passed = False

            # 日期是否为空
            if ws.cell(row=row, column=6).value:
                checking_date = ws.cell(row=row, column=6).value
            else:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='11')
                passed = False

    #         # 日期应该是日期型
    #         try:
    #             if type(checking_date) == type('123'):
    #                 result = result + '14日期须为日期型'
    #                 ws.cell(row=row, column=9).value = result
    #                 continue
    #         except Exception as e:
    #             print(e)

            # 人员是否为空
            if ws.cell(row=row, column=7).value:
                checking_author = ws.cell(row=row, column=7).value.strip()
            else:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='12')
                passed = False

            # 路径格式整理

            # '\'替换为'/'
            if '\\' in checking_path:
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='02')
                passed = False

            # https开头
            if not checking_path.startswith(tools.svn.get('server')):
                check_detail.objects.create(check_no=check_no, excel_line=row, line_name=checking_name, problem='03')
                passed = False

            if not passed:
                continue

    #         # 拼url
    #
    #         # 路径是否包含文件名
    #         # if len(checking_path)==checking_path.rfind(checking_name)+len(checking_name):
    #         if checking_path.endswith(checking_name):
    #             url = checking_path
    #         else:
    #             # 结尾有没有'/'
    #             if checking_path.endswith('/'):
    #                 url = checking_path + checking_name
    #             else:
    #                 url = checking_path + '/' + checking_name
    #
    #         # 取svn服务器信息
    #         try:
    #             entry = pysvn.Client().info2(url,
    #                                          revision=pysvn.Revision(pysvn.opt_revision_kind.number, checking_revision),
    #                                          peg_revision=pysvn.Revision(pysvn.opt_revision_kind.number,
    #                                                                      checking_revision)
    #                                          )
    #             log = pysvn.Client().log(url,
    #                                      # revision_start=pysvn.Revision( pysvn.opt_revision_kind.number,checking_revision ),
    #                                      revision_start=pysvn.Revision(pysvn.opt_revision_kind.head),
    #                                      revision_end=pysvn.Revision(pysvn.opt_revision_kind.number, checking_revision)
    #                                      )
    #         except Exception as e:
    #             print(Exception, ':', e)
    #             result = result + '04该路径源码无此版本源码'
    #             ws.cell(row=row, column=9).value = result
    #             continue
    #
    #             ##        print (entry[0][1].last_changed_author )
    #             ##        print (entry[0][1].last_changed_rev )
    #             ##        print (time.strftime('%Y/%m/%d',time.localtime(entry[0][1].last_changed_date)))
    #             ##        print (entry[0][1].kind  )
    #             ##        print (entry[0][1].URL   )
    #             ##        print (entry[0][1].rev  )
    #             ##        print (entry[0][1].repos_root_URL   )
    #             ##        print (entry[0][1].repos_UUID   )
    #             ##        print (entry[0][1].lock   )
    #             ##        print (entry[0][1].wc_info  )
    #             ##        print (time.strftime('%Y/%m/%d',time.strptime('2017/5/24','%Y/%m/%d')))
    #             ##        print ('log:'+'*'*20)
    #             ##        print (log[0].author)
    #             ##        print (log[0].date)
    #             ##        print (log[0].message)
    #             ##        print (log[0].revision.number)
    #
    #         # 检查
    #         # 是否最新版本
    #         try:
    #             log[0]
    #         except Exception as e:
    #             print(checking_path)
    #             print(Exception, ':', e)
    #             continue
    #
    #         if log[0].revision.number != checking_revision:
    #             result = result + '05源码清单登记非最新版本源码请确认'
    #         # 检查message
    #         if not ws['I5'].value:
    #             if not log[-1].message.startswith(project_name[0:15]):
    #                 result = result + '06源码上传说明建议以软件需求编号开头'
    #         else:
    #             if not log[-1].message[0:8].isdigit():
    #                 result = result + '06源码上传说明建议以软件需求编号开头'
    #         # 检查人名
    #         if entry[0][1].last_changed_author != checking_author and not entry[0][
    #             1].last_changed_author in checkauthor(checking_author, author_ws):
    #             result = result + '07开发人员应于svn上传人用户名相同'
    #         # 检查日期
    #         if checking_date.strftime('%Y-%m-%d') != time.strftime('%Y-%m-%d',
    #                                                                time.localtime(entry[0][1].last_changed_date)):
    #             result = result + '08提交日期与SVN服务器应一致'
    #         # 源码清单不应包含文件夹记录
    #         if entry[0][1].kind != pysvn.node_kind.file:
    #             result = result + '09源码清单不应包含文件夹记录'
    #
    #         # 写检查结果
    #         ws.cell(row=row, column=9).value = result
    #         ##            print(result)
    #
    # # 保存并关闭文件
    # wb.close()



##检查结果统计
##checking_temp.append(checking_name)
##checking_temp.append(checking_path)
##checking_temp.append(checking_revision)
##checking_temp.append(checking_date)
##checking_temp.append(checking_author)
##checking_temp.append(result)


'''

#更新
#pysvn.Client().update(localpath)

#新增文件，先add再checkin
#pysvn.Client().add(localpath+'test.txt')
#pysvn.Client().checkin([localpath+'test.txt'], 'test adding a sample file')

#提交更改
#pysvn.Client().checkin([localpath+'test.txt'], '中文注释')

#删除，会把本地目录的文件也删掉
#pysvn.Client().remove(localpath+'test.txt')
#pysvn.Client().checkin([localpath+'test.txt'], '删除测试')

changes = pysvn.Client().status(localpath)
print([f.text_status for f in changes])

print ('files to be added:')
print ([f.path for f in changes if f.text_status == pysvn.wc_status_kind.added])
print ('files to be removed:')
print ([f.path for f in changes if f.text_status == pysvn.wc_status_kind.deleted])
print ('files that have changed:')
print ([f.path for f in changes if f.text_status == pysvn.wc_status_kind.modified])
print ('files with merge conflicts:')
print ([f.path for f in changes if f.text_status == pysvn.wc_status_kind.conflicted])
print ('unversioned files:')
print ([f.path for f in changes if f.text_status == pysvn.wc_status_kind.unversioned])
'''

# 主程序开始

# 读配置文件
def mian():
    config_xml = 'svn_config.xml'
    try:
        fsock = open(config_xml, "r", encoding='gb18030')
    except IOError:
        print("The readfile don't exist, Please double check!")
        exit()

    # 挨行读
    AllLines = fsock.readlines()
    for EachLine in AllLines:
        a = EachLine.split('=')
        # svn服务器路径 https://10.16.80.52:8443/svn
        if a[0].strip() == 'server':
            server = a[1].strip()
            server.replace('\n', '')
            continue
        # svn用户文档路径 D:/SVN/svn_doc/2项目用户_开发.xlsx
        if a[0].strip() == 'authorpath':
            authorpath = a[1].strip()
            authorpath.replace('\n', '')
            continue
        # 源码清单评审记录文件路径 （未实装）D:/SVN/svn_doc/源码评审记录.xlsx
        if a[0].strip() == 'write_file':
            write_file = a[1].strip()
            write_file.replace('\n', '')
            continue
    fsock.close()


if __name__=='__main__':
    import svn.remote
    import svn.local
    print('=================checkresourcelist============')
    url = 'https://10.16.80.52:8443/svn/svn_doc/'
    paht = 'D:/SVN/svn_doc/'
    s = svn.remote.RemoteClient(url)
    q = svn.local.LocalClient(paht)
    # q.update()  # q 的初始化必须是个路径，不能是文件
    #
    # info
    # l = s.info(rel_path='test.txt')
    # for k in l:
    #     print('%s : %s' %(k, l.get(k)))
    #
    # log
    l = s.log_default(rel_filepath='test.txt')
    for e in l:
        print(e)
        print(e[2])




