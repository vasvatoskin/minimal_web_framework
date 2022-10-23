from my_minimal_framework.my_thread_server import MyServer

app = MyServer(port=9999)
response = "Hello World"

@app.route("/index")
def index_get():
    return response

@app.route("/index", "POST")
def index_set(body):
    global response 
    response = body
    return
    

app.run() 