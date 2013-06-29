# -*- coding: utf-8 -*-

'''要求第一次使用时前Smarthosts文件最好完整保存在hosts文件内
hosts文件内除SmartHosts内使用的 无形如"#UPDATE:XXXX-XX-XX XX:XX"样标记
'''

import httplib2
import shutil
import os
import sys
import re

# Get some data

strURL = 'http://smarthosts.googlecode.com/svn/trunk/hosts'
strPath = 'C:\\WINDOWS\\system32\\drivers\\etc\\'
listLocalHosts = []
strContent = ''

h = httplib2.Http('cache')
strResponse, bContent = h.request(strURL)

for ch in bContent.decode('utf-8'):
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

# def functions

def FindLocalTimeStamp():
	'''Find time stamp of local hosts
	'''

	strPattern = re.compile(r'#UPDATE:\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
	for strTemp in listLocalHosts:
		if len(re.findall(strPattern, strTemp)) > 0:
			strLocalTimeStamp = re.findall(strPattern, strTemp)[0]
			break

	return strLocalTimeStamp

def CmpTimeStamp():
	'''Compare Timestamp between local and remote
	'''

	strRemoteTimeStamp = bContent.decode('utf-8').split('\n')[0].rstrip()
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


if CmpTimeStamp() == False:
	print('Therer are new version in googlecode.\n')
	MakeBackup()
	UpdateHosts()
else:
	print('Your hosts is the latest version.')

# os.system("pause")