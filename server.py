import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500  # The port used by the server
ADDRESS = (HOST, PORT)

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 type TCP
listening_socket.bind(ADDRESS) # binding server addres to listening socket
listening_socket.listen()
print(f"[LISTENING] Server is listening on {ADDRESS}")
listening_socket.setblocking(False) # since we want multiple connections we set blocking on false, because we gonna block later with events
sel.register(listening_socket, selectors.EVENT_READ, data=None) # sel.register() registers the socket to be monitored with sel.select() for the events that you’re interested in. For the listening socket, you want read events: selectors.EVENT_READ.

try:
    while True:
        events = sel.select(timeout=None) # waiting for conns on registered listening_socket
        for key, mask in events:
            if key.data is None:
                #accept_wrapper(key.fileobj) #if new connection on listening socket
                pass
            else:
                #service_connection(key, mask) # if client is already connected and send smth
                pass
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
