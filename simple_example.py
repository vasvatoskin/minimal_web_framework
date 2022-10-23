from my_minimal_framework.my_thread_server import MyServer

app = MyServer(port=9999)

@app.route(target="/index")
def index():
    return "Hello World"

app.run() 