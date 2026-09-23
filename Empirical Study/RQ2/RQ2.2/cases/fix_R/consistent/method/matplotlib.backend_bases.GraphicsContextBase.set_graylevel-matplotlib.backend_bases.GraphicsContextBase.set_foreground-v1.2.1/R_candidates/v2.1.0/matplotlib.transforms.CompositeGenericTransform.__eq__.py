    def __eq__(self, other):
        if isinstance(other, (CompositeGenericTransform, CompositeAffine2D)):
            return self is other or (self._a == other._a and self._b == other._b)
        else:
            return False
