    def transform_affine(self, values):
        """
        Performs only the affine part of this transformation on the
        given array of values.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally a no-op.  In
        affine transformations, this is equivalent to
        ``transform(values)``.

        Parameters
        ----------
        values : array
            The input values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`input_dims`).

        Returns
        -------
        values : array
            The output values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`output_dims`), depending on the input.
        """
        return self.get_affine().transform(values)
