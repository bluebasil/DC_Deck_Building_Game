#import socketserver

#class MyTCPHandler(socketserver.BaseRequestHandler):
"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

"""    def handle(self):
		# self.request is the TCP socket connected to the client
		self.data = self.request.recv(1024).strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# just send back the same data, but upper-cased
		self.request.sendall(self.data.upper())

if __name__ == "__main__":
	HOST, PORT = "localhost", 3001

	# Create the server, binding to localhost on port 9999
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()"""

#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 3002        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by', addr)
		while True:
			data = conn.recv(1024)
			
			#if data != b'':
			print(f"{data}::That was the data")
			if not data:
				print("NOT ADAT")
				break
			conn.sendall(data)
