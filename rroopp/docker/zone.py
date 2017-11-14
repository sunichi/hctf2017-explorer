#! /usr/bin/python
import pwn
import os
import requests
from hashlib import sha256

token = ''
team_name = ''

def checkToken(token):
    try:
        global team_name
        res = requests.get('http://118.193.194.210:81/token/%s'%(token))
        if res.status_code == 200:
            if res.json()['status'] == 'success':
                team_name = res.json()['data']
                return 0
            else:
                return 1
        else:
            return 1
    except :
        return -1
def getFlag():
    '''
    The function to get call for get flag.You can make a different flag for different listen
    '''
    flag = sha256(token + 'ztgh4q2HlwdO').hexdigest()
    f = "congratulations " + team_name.encode('utf-8') + '\nhere is you flag: '
    f += "hctf{%s}"%(flag)
    return f

def getName(listen):
    global token
    listen.sendline('please input you token')
    token = listen.recvline()
    token = token.strip()
    r = checkToken(token)
    if r == -1:
        listen.sendline('something is wrong plz wait a moment or contact to admin')
        return False
    elif r == 1:
        listen.sendline('invalid token')
        return False
    return True
    
a = pwn.daemon(300)  # A demon class,The argument is the second of time out, 0 is no timeout

a.set_listen(12345, timeLimit=2)  # The port you want to listen
newEnv = os.environ.copy()
a.set_process('LD_PRELOAD=./libtcmalloc_minimal.so.0 ./rroopp', cwd='/home/pwn', shell=True, bin='/root/bin',env=newEnv)  # first argument is the binary,
# make sure other has permission of execute for it
a.set_sql('explorer', 'VsJ5DU6PjNh7')  # The name and password of mysql. Default it will log data in database pwnlog.
# But you can easy change it.And dot't worry of table.I will create it
a.open_permission()
a(getFlag,getName)  # start it
