import socket
HOST = '127.0.0.1'
PORT = 24680
def connectToServer(HOST, PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.connect((HOST, PORT))

	return server_socket

server_socket = None
try:
	server_socket = connectToServer(HOST, PORT)
except ConnectionRefusedError:
	print("*** Start the server first! ***")

if server_socket != None:
	while True:
		data_recvd = server_socket.recv(1024).decode('utf-8')
		print(data_recvd)

		if '>>>' in data_recvd:
			data_to_send = input()
			server_socket.sendall(data_to_send.encode('utf-8'))

		if not data_recvd:
			server_socket.close()
			break

    server_socket.close()
