import socket

HOST = "127.0.0.1"
PORT = 3000

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"||skibidi toilet 21 ||")
    data = s.recv(1024)

print(f"recived{data!r}")
