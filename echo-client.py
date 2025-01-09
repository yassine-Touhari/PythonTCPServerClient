import socket


HOST = "127.0.0.1"
PORT = 3000

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"||skibidi toilet||")
    data = s.recv(1024)

print(f"recived{data!r}")

#http request
response = "GET / HTTP/1.1"

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
# send request

client_socket.sendall(response.encode('utf-8'))



#recive response

response = client_socket.recv(4096)
print("response from server ")
print(response.decode('utf-8'))
client_socket.close()

