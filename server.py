import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500  # The port used by the server
ADDRESS = (HOST, PORT)

def accept_new_client(socket):
    user_conn, user_address = socket.accept() # accepts new connection and asign it to new socket representing conn with client
    print(f"[NEW CONNECTION] Accepted connection from {user_address}")   
    user_conn.setblocking(False)
    data = types.SimpleNamespace(addr=user_address,inb=b"", outb=b"") #  create an object to hold the data that you want included along with the socket
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # client connection is ready for reading and writing
    sel.register(user_conn, events, data=data) # registering client socket connection to be monitored

def handle_client(key, mask):
    client_socket = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = client_socket.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}") # if recv_data is empty close and unregister the client socket because client closed the conn
            sel.unregister(client_socket)
            client_socket.close()
    

def start():
    print("[STARTING] Server is starting...")

    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 type TCP
    listening_socket.bind(ADDRESS) # binding server addres to listening socket
    listening_socket.listen()
    print(f"[LISTENING] Server is listening on {ADDRESS}")
    listening_socket.setblocking(False) # since we want multiple connections we set blocking on false, because we gonna block later with events
    sel.register(listening_socket, selectors.EVENT_READ, data=None) # sel.register() registers the socket to be monitored with sel.select() for the events that you’re interested in. For the listening socket, you want read events: selectors.EVENT_READ.

    try:
        while True:
            events = sel.select(timeout=None) # waiting for: 1. new conns on listening_socket 2. already registerd sockets from already present clients
            for key, mask in events:
                if key.data is None:
                    accept_new_client(key.fileobj) #if new connection on listening socket
                    pass
                else:
                    handle_client(key, mask) # if client is already connected and send smth
                    pass
    except KeyboardInterrupt:
        print("[ABORTED] Caught keyboard interrupt, exiting")
    finally:
        sel.close()

start()