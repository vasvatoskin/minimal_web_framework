import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(("localhost", 9999))
client_sock.sendall(b"!")
data = client_sock.recv(1024)
client_sock.close()
print("Recived ", repr(data))