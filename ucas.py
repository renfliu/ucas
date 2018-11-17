#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import json

try:
    from urllib.request import urlopen, Request   # python3
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen, Request          # python2
    from urllib import urlencode


def login(username, password, prefix=False):
    url = 'http://210.77.16.21'
    resp = urlopen(url)
    respUrl = resp.url
    respHost,respSearch = respUrl.split('?')
    if 'success' in respHost:
        print("Network is connected!")
        return False
    
    if prefix:
        username = "%E5%8F%91%5C" + username
        print("user:" + username + "  pass:" + password)
    params = {
        'userId': username,
        'password': password,
        'service': '',
        'queryString': respSearch,
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'false'
    }
    data = urlencode(params).encode('utf-8')
    req = Request('http://210.77.16.21/eportal/InterFace.do?method=login', data=data)
    loginResp = urlopen(req)
    loginResult = json.loads(loginResp.read().decode('utf-8'))

    if loginResult['result'] == 'fail':
        print(loginResult['message'])
    elif loginResult['result'] == 'success':
        print('Congratulations, network is connected now!')
        return True
    else:
        print('Unknown error!') 

    return False


def logout():
    logoutUrl = 'http://210.77.16.21/eportal/InterFace.do?method=logout'
    logoutResp = urlopen(logoutUrl)
    logoutResult = json.loads(logoutResp.read().decode('utf-8'))
    print(logoutResult['message'])


def status():
    url = 'http://210.77.16.21'
    resp = urlopen(url)
    respUrl = resp.url
    respHost,respSearch = respUrl.split('?')
    if 'success' in respHost:
        print("Network is connected!")
        userUrl = 'http://210.77.16.21/eportal/InterFace.do?method=getOnlineUserInfo'
        userResp = urlopen(userUrl)
        userJson = json.loads(userResp.read().decode('utf-8'))
        print("user:" + userJson['userName'])
        return True
    else:
        print("Network not connected!")
        return False


def print_usage():
    print("")
    print("ucas.py is a python script for ucas network")
    print("usage: python[2/3] ucas.py command [params]")
    print("    commands:")
    print("        login [-p] [username] [password]")
    print("            login to ucas network, e.g. python3 ucas.py login user123 pass123")
    print("            -p, --prefix: add '发\\' before username")
    print("        logout")
    print("            logout from ucas network")
    print("        find [-s] [startRoom]")
    print("            find an account from ucas icc...")
    print("            -s, --start: start from a specific room")
    print("        status")
    print("            status of network")


def find(start=101):
    startFloor = start // 100
    startRoom = 1
    isStart = True
    for floor in range(startFloor, 9):
        if isStart:
            startRoom = start % 100
            isStart = False
        for room in range(startRoom, 20):
            for ab in {'a', 'b'}:
                user = "2{}{:0>2}{}".format(floor, room, ab)
                password = "2{}{:0>2}".format(floor, room)
                print("username:" + user + "\tpassword:" + password)
                if login(user, password):
                    return True
    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Parameter Error!")
        print_usage()
    elif sys.argv[1] == 'login':
        if sys.argv[2] == '--prefix' or sys.argv[2] == '-p':
            login(sys.argv[3], sys.argv[4], True)
        else:
            login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'find':
        start = 101
        if len(sys.argv) > 3 and ( sys.argv[2] == '--start' or sys.argv[2] == '-s'):
            start = int(sys.argv[3])
        find(start)
    elif sys.argv[1] == 'logout':
        logout()
    elif sys.argv[1] == 'status':
        status()
    else:
        print("Parameter Error!")
        print_usage()
