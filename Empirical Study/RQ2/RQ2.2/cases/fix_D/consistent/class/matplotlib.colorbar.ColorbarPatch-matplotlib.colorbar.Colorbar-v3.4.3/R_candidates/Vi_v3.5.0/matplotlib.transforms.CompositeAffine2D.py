class CompositeAffine2D(Affine2DBase):
    """
    A composite transform formed by applying transform *a* then transform *b*.

    This version is an optimization that handles the case where both *a*
    and *b* are 2D affines.
    """
    def __init__(self, a, b, **kwargs):
        """
        Create a new composite transform that is the result of
        applying `Affine2DBase` *a* then `Affine2DBase` *b*.

        You will generally not call this constructor directly but write ``a +
        b`` instead, which will automatically choose the best kind of composite
        transform instance to create.
        """
        if not a.is_affine or not b.is_affine:
            raise ValueError("'a' and 'b' must be affine transforms")
        if a.output_dims != b.input_dims:
            raise ValueError("The output dimension of 'a' must be equal to "
                             "the input dimensions of 'b'")
        self.input_dims = a.input_dims
        self.output_dims = b.output_dims

        super().__init__(**kwargs)
        self._a = a
        self._b = b
        self.set_children(a, b)
        self._mtx = None

    @property
    def depth(self):
        return self._a.depth + self._b.depth

    def _iter_break_from_left_to_right(self):
        for left, right in self._a._iter_break_from_left_to_right():
            yield left, right + self._b
        for left, right in self._b._iter_break_from_left_to_right():
            yield self._a + left, right

    __str__ = _make_str_method("_a", "_b")

    def get_matrix(self):
        # docstring inherited
        if self._invalid:
            self._mtx = np.dot(
                self._b.get_matrix(),
                self._a.get_matrix())
            self._inverted = None
            self._invalid = 0
        return self._mtx
