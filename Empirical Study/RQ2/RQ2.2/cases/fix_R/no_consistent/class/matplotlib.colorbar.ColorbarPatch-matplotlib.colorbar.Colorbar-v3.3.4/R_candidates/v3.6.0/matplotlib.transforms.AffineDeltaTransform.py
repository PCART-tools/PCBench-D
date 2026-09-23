class AffineDeltaTransform(Affine2DBase):
    r"""
    A transform wrapper for transforming displacements between pairs of points.

    This class is intended to be used to transform displacements ("position
    deltas") between pairs of points (e.g., as the ``offset_transform``
    of `.Collection`\s): given a transform ``t`` such that ``t =
    AffineDeltaTransform(t) + offset``, ``AffineDeltaTransform``
    satisfies ``AffineDeltaTransform(a - b) == AffineDeltaTransform(a) -
    AffineDeltaTransform(b)``.

    This is implemented by forcing the offset components of the transform
    matrix to zero.

    This class is experimental as of 3.3, and the API may change.
    """

    def __init__(self, transform, **kwargs):
        super().__init__(**kwargs)
        self._base_transform = transform

    __str__ = _make_str_method("_base_transform")

    def get_matrix(self):
        if self._invalid:
            self._mtx = self._base_transform.get_matrix().copy()
            self._mtx[:2, -1] = 0
        return self._mtx
