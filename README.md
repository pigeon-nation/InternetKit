	# Import the sockets submodule of InternetKit
	from internetkit.sockets.client import Socket
	
	host = 'localhost' # The target host.
	port = 8000 # The port the server is hosting on.
	
	# Create the connection object.
	conn = Socket(host, port)
	
	conn.setup() # Setup the socket.
	conn.connect() # Connect to the server.
	print('Connected!!')
	
	# Receive a message from the server.
	print('Received Message:', conn.recv())
	
	# Send a message back.
	message = input('Message to send back: ')
	conn.send(message)
	
	# Close the connection.
	conn.close()
	print('Closed conn.')
