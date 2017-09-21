#Lets program a server

import sys
import socket
import threading
from termcolor import colored, cprint

class Server():
	#Constructor
	def __init__(self, host, port):	
		self.erase = '\x1b[1A\x1b[2K' #Used for printing correctly
		self.s = socket.socket()
		self.host = host
		self.port = port
		self.s.bind((self.host, self.port))
		self.s.listen(5)
		print("Server is ready...")

	#Accept connections
	def accept(self):
		print(colored("Listening for connections on port "+str(self.port), 'blue'))
		self.c, self.addr = self.s.accept()
		print(colored("Got connection from "+self.addr[0], 'green'))

	#Send a text message to connected client
	def send_text(self, msg):
		self.c.send(msg.encode('utf-8'))	

	#recieve text messages from server
	def recieve_text(self,):
		self.recieved = self.c.recv(1024).decode('utf-8')
		return self.recieved

	#print recieved messaged
	def print_text(self):
		print(colored("Client: ", "red")+self.recieved)

	#recieve and print text for interactive chat
	def print_recieved_text(self):		
		self.recieve_text()
		#Print message and on next line print 'You: ' with colors
		print('\n'+self.erase+colored("Client: ", 'red')+self.recieved+colored("\n\nYou: ", 'cyan'), end="")

	#send text interactively
	def send_text_interactively(self, e, e1):
		while True:
			self.msgRecieved = e1.wait()
			if self.msgRecieved:
				print(colored("\nYou: ", 'cyan'), end="")
				msg = str(input())
				self.send_text(msg)
				e.set()
			else:
				e.wait()


	#recieve text interactively
	def recieve_text_interactively(self, e, e1):
		while True:
			self.msgSent = e.wait()
			if self.msgSent:
				self.print_recieved_text()
				e1.set()
			else:
				e1.wait()
			

	#run thread
	def interactive_chat(self):
		e = threading.Event()
		e1 = threading.Event()

		self.t1 = threading.Thread(target=self.send_text_interactively, args=(e, e1))
		self.t2 = threading.Thread(target=self.recieve_text_interactively, args=(e, e1))

		self.t1.start()
		self.t2.start()

		e1.set()
		e.set()


if __name__ == '__main__':
	server = Server('', 3000)
	server.accept()
	server.interactive_chat()
		
