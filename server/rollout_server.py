from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from OpenSSL import crypto
import base64

PRIVATE_KEY = open("rollout_private.pem", "r").read()
PRIVATE_KEY_PW = "rollout".encode('ascii')

def sign_software(software):
	if PRIVATE_KEY.startswith('-----BEGIN '):
		pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, PRIVATE_KEY, PRIVATE_KEY_PW)
	else:
		pkey = crypto.load_pkcs12(PRIVATE_KEY, PRIVATE_KEY_PW).get_privatekey()
    	
	sign = crypto.sign(pkey, software, "sha256")
	open('sign.sha256', 'wb').write(sign)

class ServerHandler(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def _set_json_response(self):
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

	def do_GET(self):
		logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
		if str(self.path) == "/getLatestVersionNumber":
			self.handle_GetLatestVersionNumber()
		elif str(self.path) == "/getLatestSoftware":
			self.handle_GetLatestSoftware()
		elif str(self.path) == "/getSignature":
			self.handle_GetSignature()
		else :    
			self._set_response()
			self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

	def handle_GetLatestVersionNumber(self):
		version_file = open('version_config.json')
		self._set_json_response()
		self.wfile.write(version_file.read().encode(encoding='utf_8'))
    
	def handle_GetLatestSoftware(self):
		self.send_response(200)
		self.end_headers()
		with open('software.py', 'rb') as file: 
			self.wfile.write(file.read()) # Read the file and send the contents 
            
	def handle_GetSignature(self):
		self.send_response(200)
		self.end_headers()
		
		sign_software(open('software.py', 'r').read())
		
		with open('sign.sha256', 'rb') as file: 
			self.wfile.write(file.read()) # Read the file and send the contents 

def run(server_class=HTTPServer, handler_class=ServerHandler):
    server_address = ('', 1233)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
