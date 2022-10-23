import socket
import time

class My_server:
    def __init__(self, serv_port = 9999) -> None:
        self.serv_port = serv_port
        self.cid = 0

    def run(self):
        serv_sock = self.__create_serv_sock()
        while True:
            client_sock = self.__accept_client_conn(serv_sock)
            self.__serve_client(client_sock)
            self.cid += 1

    def __create_serv_sock(self) -> socket.socket:
        serv_sock = socket.socket(socket.AF_INET,
                        socket.SOCK_STREAM,
                        proto=0)
        serv_sock.bind(('', self.serv_port))
        serv_sock.listen()
        return serv_sock

    def __accept_client_conn(self, serv_sock):
        client_sock, client_addr = serv_sock.accept()
        print(f'Client #{self.cid} connected '
              f'{client_addr[0]}:{client_addr[1]}')
        return client_sock

    def __serve_client(self, client_sock):
        request = self.__read_request(client_sock)
        if request is None:
            print(f'Client #{self.cid} unexpectedly disconnected')
        else:
            response = self.__handle_request(request)
            self.__write_response(client_sock, response)

    def __read_request(self, client_sock):
        delimiter = b'!'
        request = bytearray()
        try:
            while True:
                chunk = client_sock.recv(4)
                if not chunk:
                    return None
                
                request += chunk
                if delimiter in request:
                    return request
        except ConnectionResetError:
            return None
        except:
            raise

    def __handle_request(self, request):
        time.sleep(10)
        return request[::-1]

    def __write_response(self, client_sock, response):
        client_sock.sendall(response)
        client_sock.close()
        print(f'Client #{self.cid} has been served')


if __name__ == '__main__':
    serv = My_server()
    serv.run()
