#!/usr/bin/env python3

import threading
from .sconn import Conn
import socket

class SockServer:
	def __init__(self, host, port):
		self.host = host
		self.port = port
	
	def setup(self):
		self.sock = socket.socket()
	
	def start(self):
		self.sock.bind((self.host, self.port))
		self.sock.listen()
	
	def ut_raw_loop(self, target):
		while 1:
			conn, addr = self.sock.accept()
			threading.Thread(target=lambda: target(conn, addr)).start()
	
	def raw_loop(self, target):
		threading.Thread(target=lambda: self.ut_raw_loop(target)).start()
	
	def ut_loop(self, target):
		while 1:
			conn, addr = self.sock.accept()
			threading.Thread(target=lambda: target(Conn(conn), addr)).start()
	
	def loop(self, target):
		threading.Thread(target=lambda: self.ut_loop(target)).start()
	
	def close(self):
		self.sock.close()