import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500  # The port used by the server
ADDRESS = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.connect(ADDRESS)
    server_socket.sendall(b"Hello, world")
    data = server_socket.recv(1024)

print(f"Received {data!r}")