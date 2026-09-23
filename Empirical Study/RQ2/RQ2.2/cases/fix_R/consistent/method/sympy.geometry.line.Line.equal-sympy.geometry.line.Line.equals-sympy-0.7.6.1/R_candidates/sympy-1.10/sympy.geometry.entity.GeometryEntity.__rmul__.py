    def __rmul__(self, a):
        """Implementation of reverse multiplication method."""
        return a.__mul__(self)
