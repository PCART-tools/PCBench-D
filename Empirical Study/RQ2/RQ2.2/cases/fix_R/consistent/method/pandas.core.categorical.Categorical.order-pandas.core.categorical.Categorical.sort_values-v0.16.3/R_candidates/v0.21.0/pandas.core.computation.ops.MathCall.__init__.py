    def __init__(self, func, args):
        super(MathCall, self).__init__(func.name, args)
        self.func = func
