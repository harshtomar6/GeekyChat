#Lets program a client

import sys
import socket
import threading
from termcolor import colored, cprint

class Client:
	#Constructor
	def __init__(self, host, port):
		self.erase = '\x1b[1A\x1b[2K'
		self.s = socket.socket()
		self.host = host
		self.port = port
		self.s.connect((self.host, self.port))
		print(colored("Connected to %s on port %s" % (self.host, self.port), 'green'))

	#Send a text message to server
	def send_text(self, msg):
		self.s.send(msg.encode('utf-8'))

	#recieve text messages from server
	def recieve_text(self):
		self.recieved = self.s.recv(1024).decode('utf-8')
		return self.recieved

	#recieve and print text for interactive chat
	def print_recieved_text(self):
		self.recieve_text()
		print('\n'+self.erase+colored("Server: ", 'red')+self.recieved+colored("\n\nYou: ", 'cyan'), end="")

	#print recieved messaged
	def print_text(self):
		print(colored("Server: ","red") +self.recieved)

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
		self.t2 = threading.Thread(target=self.recieve_text_interactively, args=(e,e1))

		self.t1.start()
		self.t2.start()

		e1.set()
		e.set()


if __name__ == '__main__':
	client = Client('127.0.0.1', 3000)
	client.interactive_chat()

