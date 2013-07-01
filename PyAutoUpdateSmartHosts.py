# -*- coding: utf-8 -*-

'''要求第一次使用时前Smarthosts文件最好完整保存在hosts文件内
hosts文件内除SmartHosts内使用的 无形如"#UPDATE:XXXX-XX-XX XX:XX"样标记
'''

import httplib2
import os
import platform
import re
import shutil
import stat
import sys

# def functions

def FindLocalTimeStamp():
    '''Find time stamp of local hosts
    '''
    
    strLocalTimeStamp = ''
    strPattern = re.compile(r'#UPDATE:\d{4}-\d{2}-\d{2} \d{2}[:\D\D]\d{2}')         # ':' sometimes can't be regionsize
    for strTemp in listLocalHosts:
        if len(re.findall(strPattern, strTemp)) > 0:
            strLocalTimeStamp = re.findall(strPattern, strTemp)[0]
            break

    return strLocalTimeStamp

def CmpTimeStamp():
    '''Compare Timestamp between local and remote
    '''

    strRemoteTimeStamp = bContent.decode('gb2312').split('\n')[0].rstrip()
    strLocalTimeStamp = FindLocalTimeStamp()

    return(strRemoteTimeStamp == strLocalTimeStamp)


def MakeBackup():
    '''Make back of 'hosts' as 'hosts.bak'
    '''

    print('Now make a backup of hosts of old version.')
    shutil.copy(strPath + 'hosts', strPath + 'hosts.bak')


def UpdateHosts():
    '''Update hosts from smarthosts@googlecode
    '''

    print('Now update your hosts to the lastest version.')
    listOldHostsTail = []
    listOldHostsHead = []
    with open(strPath + 'hosts', 'r') as fileHosts:

        print('Now copy strings in your hosts before SmartHosts...')
        for strLine in fileHosts:
            if (strLine.rstrip() == FindLocalTimeStamp()):
                break
            listOldHostsHead.append(strLine)

        for strLine in fileHosts:
            if(strLine.rstrip() == '#SmartHosts END'):
                break

        print('Now copy strings in your hosts after SmartHosts...')
        for strLine in fileHosts:
            listOldHostsTail.append(strLine)

    
    with open(strPath + 'hosts.new', 'w') as fileHostsNew:

        print('Now writing...')
        
        if os.access(strPath, os.W_OK) == False:
            os.chmod(strPath, stat.S_IWUSR)             # get write right to hosts in Windows

        old_out = sys.stdout
        sys.stdout = fileHostsNew
        for strTemp in listOldHostsHead:
            sys.stdout.write(strTemp)
        sys.stdout.write(strContent)
        for strTemp in listOldHostsTail:
            sys.stdout.write(strTemp)
        sys.stdout = old_out

    os.remove(strPath + 'hosts')
    os.rename(strPath + 'hosts.new', strPath + 'hosts')
    print('\nSuccessed!')

def GetHostsPath():
    '''Find platform and return hosts's Path
    '''

    if platform.system() == 'Windows':          # deal with different platform
        if str(sys.version.split()[0])[0] == '3':           # get python version
            strPath = os.environ.__dict__['_data']['SYSTEMROOT'] + '\\system32\\drivers\\etc\\'     # deal with the situation that user's system is't installed in C:
        elif str(sys.version.split()[0])[0] == '2':
            strPath = os.environ.__dict__['data']['WINDIR'] + '\\system32\\drivers\\etc\\'
    elif platform.system() == 'Linux':
        strPath = '/etc/'

    return strPath

# Get data

strChoice = input('Input your Choice :\n1. Beijing Server\n2. US Server\n')     # choose Beijing Version or US version
strPath = GetHostsPath()
listLocalHosts = []
strContent = ''
if strChoice == '1':
    strURL = 'http://smarthosts.googlecode.com/svn/trunk/hosts'
elif strChoice == '2':
    strURL = 'http://smarthosts.googlecode.com/svn/trunk/hosts_us'

h = httplib2.Http('cache')
strResponse, bContent = h.request(strURL)

for ch in bContent.decode('gb2312'):
    if ch == '\r':
        pass
    else:
        strContent = strContent + ch

if 'hosts' in os.listdir(strPath):
    with open(strPath + 'hosts', 'r') as fileHosts:
        for strLine in fileHosts:
            listLocalHosts.append(strLine)
else:
    fileHosts = open(strPath + 'hosts', 'w')
    fileHosts.close()

# Main

if CmpTimeStamp() == False:
    print('Therer are new version in googlecode.\n')
    MakeBackup()
    UpdateHosts()
else:
    print('Your hosts is the latest version.')

shutil.rmtree(os.getcwd() + '\\cache')

os.system("pause")