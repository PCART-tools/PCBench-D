    def __call__(self, func):
        func.__doc__ = func.__doc__ and func.__doc__ % self.params
        return func
