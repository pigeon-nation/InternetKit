#!/usr/bin/env python3

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
	
	def unthreaded_connloop(self, target):
		while 1:
			conn, addr = self.sock.accept()
			threading.Thread(target=lambda: target(conn, addr)).start()
	
	def threaded_connloop(self, target):
		threading.Thread(target=lambda: self.unthreaded_connloop(target)).start()
	
	def ut_sconnloop(self, target):
		while 1:
			conn, addr = self.sock.accept()
			threading.Thread(target=lambda: target(Conn(conn), addr)).start()
	
	def sconnloop(self, target):
		threading.Thread(target=lambda: self.utcnlp(target)).start()
	
	def close(self):
		self.sock.close()