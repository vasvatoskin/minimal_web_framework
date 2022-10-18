import json
from my_error import HTTPError
from my_request import MyRequest


class MyHandler:
  def __init__(self, request: MyRequest):
    self.request = request
    self.func_map = UrlMapRoute
    
  def route(self, target: str, method: str = "GET"):
    def decorator(f):
      self.func_map.set_endpoint(target=target,
                                 method=method,
                                 func=f)
      return f
    return decorator
      
      
  def getResponse(self, req):
    if req.method == 'POST':
      return self.do_post(req)
    
    if req.method == 'GET':
      return self.do_get(req)
      
    raise HTTPError(404, 'Not found')
  
  
  def do_post(self, req:MyRequest):
    return MyResponse(204, 'Created')


  def do_get(self, req:MyRequest):
    accept = req.headers.get('Accept')
    
    if 'application/json' in accept:
      contentType = 'application/json; charset=utf-8'
      f = self.func_map.get_endpoint[req.target, req.method]
      body = f()
      
    else:
      return MyResponse(406, 'Not Acceptable')
    
    body = body.encode('utf-8')
    headers = [('Content-Type', contentType),
               ('Content-Lenght', len(body))]
    return MyResponse(200, 'OK', headers, body)
  

class MyResponse:
  def __init__(self, status, reason, headers=None, body=None):
    self.status = status
    self.reason = reason
    self.headers = headers
    self.body = body
    
class UrlMapRoute:
  def __init__(self):
    self.url_map = {}
    
  def set_endpoint(self, target, method, func):
    if method in self.url_map.keys():
      self.url_map[method][target] = func
    else:
      temp = {target: func}
      self.url_map[method] = temp
      
  def get_endpoint(self, target, method):
    return self.url_map[method][target]