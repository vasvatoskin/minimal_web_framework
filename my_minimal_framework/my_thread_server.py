import socket
import threading
from .my_request import MyParser, MyRequest
from .my_response import MyHandler, MyResponse, UrlMapRoute

class MyServer:
    def __init__(self,
                host='',
                port=9000):
        self._host = host
        self._port = port
        self._func_map = UrlMapRoute()
        
    def route(self, target: str, method: str = "GET"):
        def decorator(f):
            self._func_map.set_endpoint(target=target,
                                        method=method,
                                        func=f)
            return f
        return decorator
    
    def run(self):
        serv_sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    new_thread = threading.Thread(target=self.serve_client, args=(conn,))
                    new_thread.start()
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()


    def serve_client(self, conn):
        try:
            par = MyParser(conn)
            req: MyRequest = par.getRequest()
            hand = MyHandler(req, self._func_map)
            resp: MyResponse = hand.getResponse()
            self.send_response(conn, resp)
            conn.close()
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)
            conn.close()



    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))
        
        if resp.headers:
            for(key, value) in resp.headers:
                header_line = f'{key}: {value}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))
            
        wfile.write(b'\r\n')
        
        if resp.body:
            wfile.write(resp.body)
        
        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'
        resp = MyResponse(status, reason,
                        [('Content-Lenght', len(body))],
                        body)
        self.send_response(conn, resp)