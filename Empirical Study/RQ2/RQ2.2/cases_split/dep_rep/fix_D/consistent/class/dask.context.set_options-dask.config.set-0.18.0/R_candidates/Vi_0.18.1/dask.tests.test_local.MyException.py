    class MyException(Exception):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __str__(self):
            return "My Exception!"
