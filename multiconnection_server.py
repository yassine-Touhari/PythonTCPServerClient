import selectors
import socket

#selector object
selector = selectors.DefaultSelector()

#server host and port
HOST = "127.0.0.1"
PORT = 3000

def accept_con(server):
    """
    accept client connection and register it for reading
    :param server: server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
    client_socket, client_address = server.accept()  # to accept incoming connections
    print('accepted', client_socket, 'from', client_address)
    client_socket.setblocking(False) #setting the client socket to non bloxking mode

    #registering the client socket for reading
    selector.register(client_socket, selectors.EVENT_READ, handle_client)

def handle_client(client_socket):
    """
    echoes recieved data back to client
    :param client_socket:  client socket object

    """

    data = client_socket.recv(1024) # limiting reading to 1024 bytes from the client
    if data:
        print(f"recieved : {data.decode('utf-8')}")
        client_socket.sendall(data) # echo data back to client
    else:
        print("client disconnected")
        #unregisting the client socket when not connected
        selector.unregister(client_socket)
        client_socket.close()
#create TCP socket (maybe this should put this right after host and port definition future me make that decision for me  )
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#bind socket to the port
server.bind((HOST,PORT))
#sart listening for incoming connections
server.listen()
# Setting the server socket to non-blocking mode
server.setblocking(False)
# Register the server socket with the selector for reading events
# Associate it with the accept_con function to handle new connections
print(f'server listening on {HOST} : {PORT}')
selector.register(server,selectors.EVENT_READ,accept_con)

#server looop
while True:
    events = selector.select(timeout=None)
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)






