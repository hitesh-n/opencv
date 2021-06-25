import socket
import requests

HOST = '127.0.0.1'
PORT = 24680

def openConnection():

	client_socket = None
	client_addr = None

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((HOST, PORT))
	sock.listen(1)
	while True:
		client_socket, client_addr = sock.accept()
		if client_addr != None: break

	return client_socket, client_addr

def startCommunication(client_conn, client_addr, web_page_data):
	client_conn.sendall(bytes("Hi there, Welcome to the image recognition server!", 'utf-8'))
	client_conn.sendall(bytes(">>> Please enter the image url below : \n", 'utf-8'))

	image_url = client_conn.recv(1024).decode('utf-8')


client_conn, client_addr = openConnection()
startCommunication(client_conn, client_addr, web_page_data)
client_conn.close()
