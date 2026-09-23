    def __radd__(self, a):
        """Implementation of reverse add method."""
        return a.__add__(self)
