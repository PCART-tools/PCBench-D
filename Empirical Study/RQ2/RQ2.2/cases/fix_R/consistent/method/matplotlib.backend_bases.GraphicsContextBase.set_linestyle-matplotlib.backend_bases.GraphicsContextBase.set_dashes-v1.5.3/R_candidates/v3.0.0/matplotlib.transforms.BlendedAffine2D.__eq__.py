    def __eq__(self, other):
        # Note, this is an exact copy of BlendedGenericTransform.__eq__
        if isinstance(other, (BlendedAffine2D, BlendedGenericTransform)):
            return (self._x == other._x) and (self._y == other._y)
        elif self._x == self._y:
            return self._x == other
        else:
            return NotImplemented
