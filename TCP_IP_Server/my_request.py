from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
from my_error import HTTPError

MAX_LINE = 64*1024
MAX_HEADERS = 100

class MyParser:
  def __init__(self, connect):
    self.connect = connect

  def getRequest(self):
    rfile = self.connect.makefile('rb')
    method, target, ver = self.parse_request_line(rfile)
    headers = self.parse_headers(rfile)
    host = headers.get('Host')
    if not host:
      raise HTTPError(400, 'Bad request',
                      'Host header is missing')
    if host not in (self._server_name,
                    f'{self._server_name}:{self._port}'):
      raise HTTPError(404, 'Not found')    
    return MyRequest(method, target, ver, headers, rfile)
  
  def parse_headers(self, rfile):
    headers = []
    while True:
      line = rfile.readline(MAX_LINE + 1)
      if len(line) > MAX_LINE:
        raise HTTPError(494, 'Request header too large')
      
      if line in (b'\r\n',b'\n',b''):
        break
      
      headers.append(line)
      if len(headers) > MAX_HEADERS:
        raise HTTPError(494, 'Too many headers')
      
    sheaders = b''.join(headers).decode('iso-8859-1')
    return Parser().parsestr(sheaders)
  
  def parse_request_line(self, rfile):
    raw = rfile.readline(MAX_LINE + 1)
    if len(raw) > MAX_LINE:
      raise HTTPError(400, 'Bad request',
                      'Request line is too long')
    
    req_line = str(raw, 'iso-8859-1')
    words = req_line.split()
    if len(words) != 3:
      raise HTTPError(400, 'Host header is missing',
                      'Malformed request line')
      
    method, target, ver = words
    if ver!= 'HTTP/1.1':
      raise HTTPError(505, 'HTTP Version Not Supported')
    return method, target, ver
  

class MyRequest:
  def __init__(self, method, target, ver, headers, rfile):
    self.method = method
    self.target = target
    self.ver = ver
    self.headers = headers
    self.rfile = rfile
  
  @property
  @lru_cache(maxsize=None)
  def url(self):
    return urlparse(self.target)
  
  @property
  @lru_cache(maxsize=None)
  def query(self):
    return parse_qs(self.url.query)
  
  @property
  def path(self):
    return self.url.path
  
  def body(self):
    size = self.headers.get('Content-Lenght')
    if not size:
      return None
    return self.rfile.read(size)