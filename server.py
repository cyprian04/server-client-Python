import socket
import selectors

# Function to handle incoming connections
def handle_connections(server_socket):
    client_sockets = {}

    # Create a selector object
    selector = selectors.DefaultSelector()
    selector.register(server_socket, selectors.EVENT_READ)

    while True:
        # Wait for an activity on one of the sockets
        for key, events in selector.select():
            if key.fileobj == server_socket:
                # Accept new connection
                client_socket, client_address = server_socket.accept()
                print(f"[CONNECTION] New connection from host: {client_address}")

                # Send a welcome message to the new client
                client_socket.send("[SERVER] Welcome to the server!\n Type 'exit' to disconnect.\n".encode())

                # Register the new client socket with the selector
                selector.register(client_socket, selectors.EVENT_READ)
                client_sockets[client_socket] = client_address
            else:
                # Receive and echo messages back to the client
                client_socket = key.fileobj
                try:
                    data = client_socket.recv(1024)
                    if data:
                        message = data.decode()
                        print(f"Received message from {client_sockets[client_socket]}: {message}")

                        # Echo the message back to the same client
                        client_socket.send(data)
                    else:
                        # Remove the disconnected client
                        print(f"Connection closed by {client_sockets[client_socket]}")
                        selector.unregister(client_socket)
                        del client_sockets[client_socket]
                except:
                    continue

# Main function to set up the server
def main():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 8888)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen()
    print("[LISTENING] Server is listening on {}:{}".format(*server_address))

    # Handle incoming connections
    handle_connections(server_socket)

if __name__ == "__main__":
    main()
