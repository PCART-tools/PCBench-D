    def transform_non_affine(self, values):
        """
        Apply only the non-affine part of this transformation.

        ``transform(values)`` is always equivalent to
        ``transform_affine(transform_non_affine(values))``.

        In non-affine transformations, this is generally equivalent to
        ``transform(values)``.  In affine transformations, this is
        always a no-op.

        Parameters
        ----------
        values : array
            The input values as NumPy array of length :attr:`input_dims` or
            shape (N x :attr:`input_dims`).

        Returns
        -------
        array
            The output values as NumPy array of length :attr:`output_dims` or
            shape (N x :attr:`output_dims`), depending on the input.
        """
        return values
