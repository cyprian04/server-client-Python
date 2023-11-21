import socket

PORT = 5100
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(HOST, PORT)



print("[STARTING] server is starting...")