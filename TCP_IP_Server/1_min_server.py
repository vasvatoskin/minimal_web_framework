import socket

serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_soc.bind(("127.0.0.1", 9999))
serv_soc.listen(100)

while True:
    client_soc, client_addr = serv_soc.accept()
    print("Connected by ", client_addr)

    while True:
        data = client_soc.recv(1024)
        if not data:
            break
        if data == b'ping':
            client_soc.sendall(b'pong')
            client_soc.close

    client_soc.close