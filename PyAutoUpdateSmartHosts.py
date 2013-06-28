# -*- coding: utf-8 -*-

'''默认hosts文件第一部分来自smarthosts，后边随意
'''

import httplib2
import shutil
import os

# Get some data

strURL = 'https://smarthosts.googlecode.com/svn/trunk/hosts'
strPath = 'C:\\WINDOWS\\system32\\drivers\\etc\\'
listRemoteHosts = []

h = httplib2.Http('cache')
strResponse, bContent = h.request(strURL)

if 'hosts' in os.listdir(strPath):
	with open(strPath + 'hosts', 'r') as fileHosts:
		for strLine in fileHosts:
			listRemoteHosts.append(strLine)
else:
	fileHosts = open(strPath + 'hosts', 'w')
	fileHosts.close()

# def functions

def CmpTimeStamp():
	'''Compare Timestamp between local and remote
	'''

	strRemoteTimeStamp = bContent.decode('utf-8').split('\n')[0].rstrip()

	strLocalTimeStamp = listRemoteHosts[0].rstrip()

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
	listOldHosts = []
	with open(strPath + 'hosts', 'r') as fileHosts:

		for strLine in fileHosts:
			if(strLine.rstrip() == '#SmartHosts END'):
				break
		for strLine in fileHosts:
			listOldHosts.append(strLine)

	
	with open(strPath + 'hosts.new', 'w') as fileHostsNew:
		for strTemp in listRemoteHosts:
			fileHostsNew.write(strTemp)
		for strTemp in listOldHosts:
			fileHostsNew.write(strTemp)

	os.remove(strPath + 'hosts')
	os.rename(strPath + 'hosts.new', strPath + 'hosts')


if __name__ == '__main__':
	if CmpTimeStamp() == False:
		print('Therer are new version in googlecode.')
		MakeBackup()
		UpdateHosts()
	else:
		print('Your hosts is the latest version.')
