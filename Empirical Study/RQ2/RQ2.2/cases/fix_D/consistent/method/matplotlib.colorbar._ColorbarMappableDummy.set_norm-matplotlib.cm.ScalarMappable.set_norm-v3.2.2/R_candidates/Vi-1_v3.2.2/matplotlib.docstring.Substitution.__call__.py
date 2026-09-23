    def __call__(self, func):
        if func.__doc__:
            func.__doc__ %= self.params
        return func
