import socket

s = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)
s.bind(("127.0.0.1", 45000))
s.listen()

connection, addr = s.accept()
print(f"got connection from {addr}")
while True:
    data = connection.recv(1024)
    print(data)
