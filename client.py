import socket
import sys
import select

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    client_socket.connect(server_address)
    print(f"[CONNECTION] Connected to Server: {server_address}")
    client_socket.setblocking(False)

    while True:# Wait for an activity on the socket or stdin
        try:
            readable, _, _ = select.select([client_socket], [], [], 0.1)
        except select.error as e:
            print(str(e))
            break

        for sock in readable: # readable is a list of active sockets(for reading)
            if sock == client_socket:# Receive and print messages from the server
                data = client_socket.recv(1024)
                if not data:
                    print("[CLOSING] Disconnected from the server.")
                    sys.exit()
                else:
                    print("[MESSAGE] Received message: {}".format(data.decode()))

        try: # Check if there is input from the user
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
