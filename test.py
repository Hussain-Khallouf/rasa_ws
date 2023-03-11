

class A:
    a = 5
    def __init__(self, name):
        print(name)
        self.a = 10


a = A()

print(a.a)