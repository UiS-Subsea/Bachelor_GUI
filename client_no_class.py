import socket

s = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)

conn = s.connect(("127.0.0.1", 45000))

while True:
    s.sendall(input("msg:").encode("utf-8"))