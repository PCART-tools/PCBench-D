class _BlendedMixin:
    """Common methods for `BlendedGenericTransform` and `BlendedAffine2D`."""

    def __eq__(self, other):
        if isinstance(other, (BlendedAffine2D, BlendedGenericTransform)):
            return (self._x == other._x) and (self._y == other._y)
        elif self._x == self._y:
            return self._x == other
        else:
            return NotImplemented

    def contains_branch_seperately(self, transform):
        return (self._x.contains_branch(transform),
                self._y.contains_branch(transform))

    __str__ = _make_str_method("_x", "_y")
