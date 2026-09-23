    def transform_affine(self, values):
        """
        Performs only the affine part of this transformation on the
        given array of values.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally a no-op.  In
        affine transformations, this is equivalent to
        ``transform(values)``.

        Accepts a numpy array of shape (N x :attr:`input_dims`) and
        returns a numpy array of shape (N x :attr:`output_dims`).

        Alternatively, accepts a numpy array of length :attr:`input_dims`
        and returns a numpy array of length :attr:`output_dims`.
        """
        return self.get_affine().transform(values)
