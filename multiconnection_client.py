import selectors
import socket
import types

selector = selectors.DefaultSelector()
messages = [b"w rizz" , b"L rizz"]
HOST = "127.0.0.1"
PORT = 3000
num_connections = 5
#client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def start_connection(num_connections):
    """
     Start multiple client connections to the server.
    :param num_connections:
    """
    server_address = (HOST,PORT)
    for i in range (0, num_connections):
        conn_id = i + 1
        print(f"starting connection {conn_id} to {server_address}")


        #create new socket for each connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setblocking(False)
        client_socket.connect_ex(server_address)
        #read and write events
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        data = types.SimpleNamespace (
            connid=conn_id,   # connection id
            msg_total=sum(len(m) for m in messages), #length of messages (total)
            recv_total=0,
            messages=messages.copy(), #copyy of datat to send
            outb=b"", #datat to send buffer
        )
        #register the socket with the selctor
        selector.register(client_socket, events, data=data)
def service_connection(key,mask):

    """
    handles events for a connection
    :param key:   The key containing file object and associated data
    :param mask: The event mask indicating readiness for read/write
    :return:
    """

    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection {data.connid}")
            selector.unregister(sock)
            sock.close()

        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0) #loading the next message into the outgoing buffer
            if data.outb:
                print(f"Sending {data.outb!r} to connection {data.connid}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

start_connection(num_connections)
while True:
    events = selector.select(timeout=None)
    for key, mask in events:
        service_connection(key,mask)