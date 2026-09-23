    def __init__(self, a, b, **kwargs):
        """
        Create a new composite transform that is the result of
        applying transform *a* then transform *b*.

        Both *a* and *b* must be instances of :class:`Affine2DBase`.

        You will generally not call this constructor directly but use the
        `composite_transform_factory` function instead, which can automatically
        choose the best kind of composite transform instance to create.
        """
        if not a.is_affine or not b.is_affine:
            raise ValueError("'a' and 'b' must be affine transforms")
        if a.output_dims != b.input_dims:
            raise ValueError("The output dimension of 'a' must be equal to "
                             "the input dimensions of 'b'")
        self.input_dims = a.input_dims
        self.output_dims = b.output_dims

        Affine2DBase.__init__(self, **kwargs)
        self._a = a
        self._b = b
        self.set_children(a, b)
        self._mtx = None
