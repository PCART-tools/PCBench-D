    def __reduce__(self):
        return type(self), (self.name,)
