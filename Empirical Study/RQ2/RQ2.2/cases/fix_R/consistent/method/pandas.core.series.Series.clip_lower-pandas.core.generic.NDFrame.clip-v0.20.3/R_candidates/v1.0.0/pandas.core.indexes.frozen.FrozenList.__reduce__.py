    def __reduce__(self):
        return type(self), (list(self),)
