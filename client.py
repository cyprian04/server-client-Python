import socket
import sys
import select

def main():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 8888)
    client_socket.connect(server_address)
    print(f"[CONNECTION] Connected to Server: {server_address}")

    # Set the socket to non-blocking mode
    client_socket.setblocking(False)

    while True:
        # Wait for an activity on the socket or stdin
        try:
            readable, _, _ = select.select([client_socket], [], [], 0.1)
        except select.error as e:
            break

        for sock in readable:
            if sock == client_socket:
                # Receive and print messages from the server
                data = client_socket.recv(1024)
                if not data:
                    print("[CLOSING] Disconnected from the server.")
                    sys.exit()
                else:
                    print("[MESSAGE] Received message: {}".format(data.decode()))

        # Check if there is input from the user
        try:
            message = sys.stdin.readline()
        except KeyboardInterrupt:
            print("Exiting the client.")
            sys.exit()

        if message.strip().lower() == 'exit':
            print("Exiting the client.")
            sys.exit()
        elif message:
            client_socket.send(message.encode())

if __name__ == "__main__":
    main()
