import json
from .my_error import HTTPError
from .my_request import MyRequest

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

class MyHandler:
  def __init__(self, request: MyRequest, url_map: UrlMapRoute):
    self.req = request
    self.func_map = url_map
      
  def getResponse(self):
    if self.req.method == 'POST':
      return self.do_post(self.req)
    
    if self.req.method == 'GET':
      return self.do_get(self.req)
      
    raise HTTPError(404, 'Not found')
  
  
  def do_post(self, req:MyRequest):
    f = self.func_map.get_endpoint(req.target, req.method)
    body = req.body
    f(body)
    return MyResponse(204, 'Created')


  def do_get(self, req:MyRequest):
    accept = req.headers.get('Accept')
    
    if 'application/json' in accept:
      contentType = 'application/json; charset=utf-8'
      f = self.func_map.get_endpoint(req.target, req.method)
      body = f()
      body = json.dumps(body)
      
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