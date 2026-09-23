    def __radd__(self, other):
        if isinstance(other, tuple):
            other = list(other)
        return type(self)(other + list(self))
