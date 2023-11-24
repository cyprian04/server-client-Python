import socket
import selectors

# Function to handle incoming connections
def handle_connections(server_socket):
    client_sockets = {}
    selector = selectors.DefaultSelector()
    selector.register(server_socket, selectors.EVENT_READ)

    while True:# Wait for an activity on one of the sockets
        for key, events in selector.select(): # returns a list of active sockets
            if key.fileobj == server_socket:# Accept new connection

                client_socket, client_address = server_socket.accept()
                print(f"[CONNECTION] New connection from host: {client_address}")
                client_socket.send("[SERVER] Welcome to the server!\n Type 'exit' to disconnect.\n".encode())

                selector.register(client_socket, selectors.EVENT_READ)
                client_sockets[client_socket] = client_address
            else:
                client_socket = key.fileobj# Receive and echo messages back to the client
                try:
                    data = client_socket.recv(1024)
                    if data:
                        message = data.decode()
                        print(f"[MESSAGE] Received message from {client_sockets[client_socket]}: {message}")
                        client_socket.send(data) # Echo the message back to the same client
                    else:
                        print(f"[DISCONNECTED] Connection closed by {client_sockets[client_socket]}")
                        selector.unregister(client_socket)# Remove the disconnected client
                        del client_sockets[client_socket]
                except:
                    continue

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    HOST = socket.gethostbyname(socket.gethostname())
    server_address = (HOST, 8888)
    server_socket.bind(server_address)
    server_socket.listen()
    print("[LISTENING] Server is listening on {}:{}".format(*server_address))
    handle_connections(server_socket)

if __name__ == "__main__":
    main()
