import http.client
import requests
import json
import time
import subprocess
import base64
from OpenSSL import crypto

key_file = open("rollout_public.pem", "r")
PUBLIC_KEY = key_file.read()
key_file.close()

def getLatestSoftwareVersionNumber():
	request = requests.get("http://192.168.7.1:1233/getLatestVersionNumber")
	data = json.loads(request.content)
    
	return data['latestVersion']

def getLatestSoftware():
	request = requests.get("http://192.168.7.1:1233/getLatestSoftware")
	open('software_downloaded.py', 'wb').write(request.content)
	
	if isSoftwareDownloadedValid():
		updateSoftware()
	
def readCurrentVersion():
	version_file = open('software_info.json')
	data = json.loads(version_file.read())
	
	version_file.close()
    
	return data['currentVersion']
	
def updateCurrentVersion(version):
	data = json.loads(open('software_info.json', 'r').read())
	data['currentVersion'] = version
	
	open('software_info.json', 'w').write(json.dumps(data))
	logToFile(f"Software updated from version {currentVersion} to {latestVersion}")
	
def isSoftwareDownloadedValid():
	request = requests.get("http://192.168.7.1:1233/getSignature")
	signature = request.content
    	
	pkey = crypto.load_publickey(crypto.FILETYPE_PEM, PUBLIC_KEY)

	x509 = crypto.X509()
	x509.set_pubkey(pkey)

	try:
		crypto.verify(x509, signature, open('software_downloaded.py', 'rb').read(), 'sha256')
	except:
		logToFile("Verify FAIL")
		return False
	
	logToFile("Verify OK")
	return True

	
def updateSoftware():
	with open('software_downloaded.py', 'rb') as file: 
		open('software.py', 'wb').write(file.read())
	
	updateCurrentVersion(latestVersion)

def logToFile(log):
	timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
	open('software_update.log', 'a').write(f"{timestamp} - {log}\n")
	print(f"{timestamp} - {log}\n")

while(True):
	latestVersion = getLatestSoftwareVersionNumber()
	currentVersion = readCurrentVersion()
	
	timestamp = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())

	if (latestVersion > currentVersion):
		getLatestSoftware()
	else:
		logToFile(f"Software is up-to-date with version {currentVersion}")
    	
	time.sleep(5)
    
version_file.close()
