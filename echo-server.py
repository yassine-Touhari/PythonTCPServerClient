# opening a port


import socket



# server

HOST = "127.0.0.1"
PORT = 3000

#to create  a socket
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    print("||socket created||")
    print(f"server is listening on {HOST} : {PORT} ")


    while True:
        client_socket, client_address = s.accept()

        print(f"connected by {client_address}")

        client_socket.sendall(b"hello,client!!")


        #RECIVE DATA FROM CLIENT
        data = client_socket.recv(1024)
        if data:
            print(f"from client : {data.decode('utf-8')}")
        client_socket.close()
