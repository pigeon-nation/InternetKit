#!/usr/bin/env python3

import json
import copy

class JRMCServer:
	#####################
	# Pre-Server-Start. #
	#####################
	
	# Init
	
	def __init__(self):
		self.reset()
		
	# Wrapper
		
	def reg(self, name):
		def regwrap(func):
			def registerinner(*args, **kwargs):
				res = func(*args, **kwargs)
				return res
			self.register(registerinner, name)
			return registerinner
		return regwrap
	
	# Easy Methods
	
	def register(self, func, name):
		self.mthds[name] = func
	
	def getfunc(self, name):
		return self.mthds[name]
	
	def delfunc(self, name):
		del self.mthds[name]
	
	# Special Methods
	
	def __getitem__(self, item):
		self.getfunc(item)
	
	def __setitem__(self, item, value):
		self.register(item, value)
	
	def __delitem__(self, item):
		self.delfunc(item)
		
	# Other
	
	def reset(self):
		self.conn = None
		self.addr = None
		self.mthds = {}
	
	def fail(self, info, etyp):
		return [inf, etyp] # todo - add more info.

class JRMCConnection:
	def __init__(self, conn, addr, server):
		self.server = copy.deepcopy(server)
		self.session = {}
		self.conn = conn
		self.addr = addr
		self.commence()
		
	
	#####################
	# Post-Server-Start #
	#####################
	
	def commence(self):
		while 1:
			if self.handle(self.conn.recv()):
				break
	
	def handle(self, msg):
		req = json.loads(msg)
		
		if req['request'] == 'close':
			self.conn.close()
			return True # tell the commence(...) that the connection is closed. 
		elif req['request'] == 'listmethods':
			self.conn.send(json.dumps(self.server.mthds.keys()))
			return False
		elif req['request'] == 'exec':
			try:
				mthd = self.server[req['method']]
				args = self.server[req['args']]
				kwgs = self.server[req['kwargs']]
			except:
				self.conn.send(json.dumps(self.server.fail('Invalid Request.', 'invld-req')))
			else:
				try:
					res = mthd(*args, **kwargs)
				except:
					self.conn.send(json.dumps(self.server.fail('Server Side Error - Check if your args and/or kwargs are valid.', 'srv-side')))
				else:
					if req['return']:
						self.conn.send(json.dumps(res))
				
			return False
		elif req['req'] == 'tempstore':
			if len(req['data']) < 67:
				if len(req['label']) < 67:
					if len(self.session.keys()) < 8:
						self.session[json.loads(req['label'])] = json.loads(req['data'])
					else:
						self.conn.send(json.dumps(self.server.fail('Too many currently stored data samples. Limit is 7.', 'dt-tm')))
				else:
					self.conn.send(json.dumps(self.server.fail('Label too long. Limit is 66.', 'dt-lb-tl')))
			else:
				self.conn.send(json.dumps(self.server.fail('Data too long. Limit is 66.', 'dt-dt-tl')))
			
			return False