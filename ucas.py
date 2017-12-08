#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import requests


def login(username, password, prefix=False):
    url = 'http://210.77.16.21'
    r = requests.get(url)
    resUrl = r.url
    resHost,resSearch = resUrl.split('?')
    if 'success' in resHost:
        print("网络已连接!")
        exit()
    else:
        if prefix:
            username = "%E5%8F%91%5C" + username
            print("user:" + username + "  pass:" + password)
        params = {
            'userId': username,
            'password': password,
            'service': '',
            'queryString': resSearch,
            'operatorPwd': '',
            'operatorUserId': '',
            'validcode': ''
        };
        loginResp = requests.post('http://210.77.16.21/eportal/InterFace.do?method=login', data=params)
        loginResp.encoding = 'utf-8'
        loginResult = loginResp.json()
        if loginResult['result'] == 'fail':
            print(loginResult['message'])
        elif loginResult['result'] == 'success':
            print('网络登录成功！')
            return True
        else:
            print('未知错误！') 
    return False


def logout():
    logoutUrl = 'http://210.77.16.21/eportal/InterFace.do?method=logout'
    logoutRresp = requests.get(logoutUrl)
    logoutRresp.encoding = 'utf-8'
    result = logoutRresp.json()
    print(result['message'])


def print_usage():
    print("")
    print("ucas.py is a command interface for ucas web")
    print("usage: python[3] ucas.py [OPTION [params]]")
    print("    login [-p] [username] [password]")
    print("            login to ucas network, e.g. python ucas.py user123 pass123")
    print("            -p, --prefix: add '发\\' before username")
    print("    logout")
    print("            logout from ucas network")
    print("    find")
    print("            find a user automatically")


def find(skip=0):
    for floor in range(1, 8):
        for room in range(1, 15):
            for ab in {'a', 'b'}:
                user = "2{}{:0>2}{}".format(floor, room, ab)
                password = "2{}{:0>2}".format(floor, room)
                print("user:" + user + " pass:" + password)
                if login(user, password):
                    skip -= 1
                    if skip <= 0:
                        return True
                    else:
                        logout()
    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("参数错误!")
        print_usage()
    elif sys.argv[1] == 'login':
        if sys.argv[2] == '--prefix' or sys.argv[2] == '-p':
            login(sys.argv[3], sys.argv[4], True)
        else:
            login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'logout':
        logout()
    elif sys.argv[1] == 'find':
        skip = 0
        if len(sys.argv) > 3 and sys.argv[2] == '--skip':
            skip = int(sys.argv[3])
        find(skip)
    else:
        print("参数错误!")
        print_usage()
