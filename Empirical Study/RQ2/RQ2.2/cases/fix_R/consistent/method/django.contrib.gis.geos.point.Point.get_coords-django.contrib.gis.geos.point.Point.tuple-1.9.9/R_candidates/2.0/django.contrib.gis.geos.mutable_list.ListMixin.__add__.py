    def __add__(self, other):
        'add another list-like object'
        return self.__class__(list(self) + list(other))
