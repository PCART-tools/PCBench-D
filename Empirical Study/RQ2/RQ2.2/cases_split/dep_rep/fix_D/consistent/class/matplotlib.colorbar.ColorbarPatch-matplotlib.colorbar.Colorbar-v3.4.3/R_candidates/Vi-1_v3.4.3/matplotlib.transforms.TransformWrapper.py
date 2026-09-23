class TransformWrapper(Transform):
    """
    A helper class that holds a single child transform and acts
    equivalently to it.

    This is useful if a node of the transform tree must be replaced at
    run time with a transform of a different type.  This class allows
    that replacement to correctly trigger invalidation.

    `TransformWrapper` instances must have the same input and output dimensions
    during their entire lifetime, so the child transform may only be replaced
    with another child transform of the same dimensions.
    """

    pass_through = True

    def __init__(self, child):
        """
        *child*: A `Transform` instance.  This child may later
        be replaced with :meth:`set`.
        """
        _api.check_isinstance(Transform, child=child)
        self._init(child)
        self.set_children(child)

    def _init(self, child):
        Transform.__init__(self)
        self.input_dims = child.input_dims
        self.output_dims = child.output_dims
        self._set(child)
        self._invalid = 0

    def __eq__(self, other):
        return self._child.__eq__(other)

    __str__ = _make_str_method("_child")

    def frozen(self):
        # docstring inherited
        return self._child.frozen()

    def _set(self, child):
        self._child = child

        self.transform = child.transform
        self.transform_affine = child.transform_affine
        self.transform_non_affine = child.transform_non_affine
        self.transform_path = child.transform_path
        self.transform_path_affine = child.transform_path_affine
        self.transform_path_non_affine = child.transform_path_non_affine
        self.get_affine = child.get_affine
        self.inverted = child.inverted
        self.get_matrix = child.get_matrix

        # note we do not wrap other properties here since the transform's
        # child can be changed with WrappedTransform.set and so checking
        # is_affine and other such properties may be dangerous.

    def set(self, child):
        """
        Replace the current child of this transform with another one.

        The new child must have the same number of input and output
        dimensions as the current child.
        """
        if (child.input_dims != self.input_dims or
                child.output_dims != self.output_dims):
            raise ValueError(
                "The new child must have the same number of input and output "
                "dimensions as the current child")

        self.set_children(child)
        self._set(child)

        self._invalid = 0
        self.invalidate()
        self._invalid = 0

    is_affine = property(lambda self: self._child.is_affine)
    is_separable = property(lambda self: self._child.is_separable)
    has_inverse = property(lambda self: self._child.has_inverse)
