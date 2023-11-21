import socket

PORT = 5100
HOST = socket.gethostbyname(socket.gethostname())
ADDRESS = (HOST, PORT)

print("[STARTING] server is starting...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: # same as using in c#
    server_socket.bind(HOST, PORT)
    server_socket.listen()
    user_conn, user_addr = server_socket.accept()
    with user_conn: # if socket(connection with client) is open
        print(f"Connection estabilished with {user_addr}")
        while True:
            data = user_conn.recv(1024)
            if not data: # if empty then the client shut down the connection
                break
            user_conn.sendall(data)
