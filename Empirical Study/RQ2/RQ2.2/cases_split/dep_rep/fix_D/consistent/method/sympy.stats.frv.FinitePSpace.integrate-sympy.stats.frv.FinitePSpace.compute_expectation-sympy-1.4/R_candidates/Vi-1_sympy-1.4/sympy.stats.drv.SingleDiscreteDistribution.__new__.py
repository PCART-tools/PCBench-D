    def __new__(cls, *args):
        args = list(map(sympify, args))
        return Basic.__new__(cls, *args)
