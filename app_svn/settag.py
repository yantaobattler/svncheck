# -*-coding:utf-8-*-
# !/usr/bin/env Python
# coding=utf-8


import subprocess
import svn.remote
from app_svn.models import tag_log


def settag_action(req_list):
    # 先看V存不存在
    try:
        svn.remote.RemoteClient(req_list['tag_url']).info()
        msg = req_list['v_version'] + '已存在！'
        tag_log1(req_list, 'R', msg)
        return msg
    except:
        pass

    # 再tag
    cmd = 'svn copy '
    cmd += req_list['trunk_url'] + ' '
    cmd += req_list['tag_url'] + ' '
    cmd += '-r ' + req_list['svn_version'] + ' '

    msg = '"' + req_list['UD_FD_code'] + ' '
    msg += req_list['sub_req_code'] + ' '
    msg += req_list['sub_req_name'] + ' '
    msg += 'svn:' + req_list['svn_version'] + '"'

    cmd += '-m ' + msg

    try:
        server_info = subprocess.check_output(cmd)
        msg = server_info.decode()
        tag_log1(req_list, 'S', msg)
    except:
        msg = '复制失败！请检查目录是否存在'
        tag_log1(req_list, 'R', msg)

    return msg


def tag_log1(req_list, stat, msg):
    tag_log.objects.create(sys_name     = req_list['sys_name'],
                           svn_version  = req_list['svn_version'],
                           v_version    = req_list['v_version'],
                           UD_FD_code   = req_list['UD_FD_code'],
                           trunk_url    = req_list['trunk_url'],
                           tag_url      = req_list['tag_url'],
                           sub_req_code = req_list['sub_req_code'],
                           sub_req_name = req_list['sub_req_name'],
                           user         = req_list['user'],
                           stat         = stat,
                           msg          = msg)
