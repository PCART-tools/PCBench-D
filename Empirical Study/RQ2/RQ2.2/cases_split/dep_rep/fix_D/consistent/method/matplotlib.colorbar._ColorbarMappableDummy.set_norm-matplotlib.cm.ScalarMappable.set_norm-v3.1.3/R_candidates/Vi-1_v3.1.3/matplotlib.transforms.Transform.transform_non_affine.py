    def transform_non_affine(self, values):
        """
        Performs only the non-affine part of the transformation.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally equivalent to
        ``transform(values)``.  In affine transformations, this is
        always a no-op.

        Accepts a numpy array of shape (N x :attr:`input_dims`) and
        returns a numpy array of shape (N x :attr:`output_dims`).

        Alternatively, accepts a numpy array of length :attr:`input_dims`
        and returns a numpy array of length :attr:`output_dims`.
        """
        return values
