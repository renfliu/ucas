#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import sys


def login(username, password):
    url = 'http://210.77.16.21'
    r = requests.get(url)
    resUrl = r.url
    resHost,resSearch = resUrl.split('?')
    if 'success' in resHost:
        print("网络已连接!")
        exit()
    else:
        params = {
            'userId': username,
            'password': password,
            'service': '',
            'queryString': resSearch,
            'operatorPwd': '',
            'validcode': ''
        };
        loginResp = requests.post('http://210.77.16.21/eportal/InterFace.do?method=login', data=params)
        loginResp.encoding = 'utf-8'
        loginResult = loginResp.json()
        if loginResult['result'] == 'fail':
            print(loginResult['message'])
        elif loginResult['result'] == 'success':
            print('网络登录成功！')
        else:
            print('为知错误！') 


def logout():
    logoutUrl = 'http://210.77.16.21/eportal/InterFace.do?method=logout'
    logoutR = requests.get(logoutUrl)
    logoutR.encoding = 'utf-8'
    result = logoutR.json()
    print(result['message'])


def print_usage():
    print("")
    print("ucas.py is a command interface for ucas web")
    print("usage: python[3] ucas.py [OPTION [params]]")
    print("    -i, --login  [username] [password]")
    print("            login to ucas network")
    print("    -o, --logout")
    print("            logout from ucas network")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("参数错误!")
        print_usage()
    elif sys.argv[1] == '--login' or sys.argv[1] == '-i':
        login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == '--logout' or sys.argv[1] == '-o':
        logout()
    else:
        print("参数错误!")
        print_usage()
