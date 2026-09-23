class CompositeGenericTransform(Transform):
    """
    A composite transform formed by applying transform *a* then
    transform *b*.

    This "generic" version can handle any two arbitrary
    transformations.
    """
    pass_through = True

    def __init__(self, a, b, **kwargs):
        """
        Create a new composite transform that is the result of
        applying transform *a* then transform *b*.

        You will generally not call this constructor directly but write ``a +
        b`` instead, which will automatically choose the best kind of composite
        transform instance to create.
        """
        if a.output_dims != b.input_dims:
            raise ValueError("The output dimension of 'a' must be equal to "
                             "the input dimensions of 'b'")
        self.input_dims = a.input_dims
        self.output_dims = b.output_dims

        super().__init__(**kwargs)
        self._a = a
        self._b = b
        self.set_children(a, b)

    def frozen(self):
        # docstring inherited
        self._invalid = 0
        frozen = composite_transform_factory(
            self._a.frozen(), self._b.frozen())
        if not isinstance(frozen, CompositeGenericTransform):
            return frozen.frozen()
        return frozen

    def _invalidate_internal(self, value, invalidating_node):
        # In some cases for a composite transform, an invalidating call to
        # AFFINE_ONLY needs to be extended to invalidate the NON_AFFINE part
        # too. These cases are when the right hand transform is non-affine and
        # either:
        # (a) the left hand transform is non affine
        # (b) it is the left hand node which has triggered the invalidation
        if (value == Transform.INVALID_AFFINE and
                not self._b.is_affine and
                (not self._a.is_affine or invalidating_node is self._a)):
            value = Transform.INVALID

        super()._invalidate_internal(value=value,
                                     invalidating_node=invalidating_node)

    def __eq__(self, other):
        if isinstance(other, (CompositeGenericTransform, CompositeAffine2D)):
            return self is other or (self._a == other._a
                                     and self._b == other._b)
        else:
            return False

    def _iter_break_from_left_to_right(self):
        for left, right in self._a._iter_break_from_left_to_right():
            yield left, right + self._b
        for left, right in self._b._iter_break_from_left_to_right():
            yield self._a + left, right

    depth = property(lambda self: self._a.depth + self._b.depth)
    is_affine = property(lambda self: self._a.is_affine and self._b.is_affine)
    is_separable = property(
        lambda self: self._a.is_separable and self._b.is_separable)
    has_inverse = property(
        lambda self: self._a.has_inverse and self._b.has_inverse)

    __str__ = _make_str_method("_a", "_b")

    def transform_affine(self, points):
        # docstring inherited
        return self.get_affine().transform(points)

    def transform_non_affine(self, points):
        # docstring inherited
        if self._a.is_affine and self._b.is_affine:
            return points
        elif not self._a.is_affine and self._b.is_affine:
            return self._a.transform_non_affine(points)
        else:
            return self._b.transform_non_affine(
                                self._a.transform(points))

    def transform_path_non_affine(self, path):
        # docstring inherited
        if self._a.is_affine and self._b.is_affine:
            return path
        elif not self._a.is_affine and self._b.is_affine:
            return self._a.transform_path_non_affine(path)
        else:
            return self._b.transform_path_non_affine(
                                    self._a.transform_path(path))

    def get_affine(self):
        # docstring inherited
        if not self._b.is_affine:
            return self._b.get_affine()
        else:
            return Affine2D(np.dot(self._b.get_affine().get_matrix(),
                                   self._a.get_affine().get_matrix()))

    def inverted(self):
        # docstring inherited
        return CompositeGenericTransform(
            self._b.inverted(), self._a.inverted())
