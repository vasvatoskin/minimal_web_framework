"""This module is not directly related to the project.
I am writing this project solely for self-education. Therefore, I placed 
the most visual demonstration of routing operation using decorators."""


class Router():
    def __init__(self) -> None:
        self.functions_list = {}
        
    def router(self, rule):
        def decorator(f):
            self.functions_list[rule] = f
            return f
        return decorator
    
    def getFunc(self, rule):
        return self.functions_list[rule]

if __name__ == "__main__":
    
    app = Router()
    
    @app.router('1')
    def f_1():
        print("one")
        
    @app.router('2')
    def f_2():
        print("two")

    @app.router('3')
    def f_3():
        print("three")
        
    while True:
        x = input('')
        f = app.getFunc(x)
        f()