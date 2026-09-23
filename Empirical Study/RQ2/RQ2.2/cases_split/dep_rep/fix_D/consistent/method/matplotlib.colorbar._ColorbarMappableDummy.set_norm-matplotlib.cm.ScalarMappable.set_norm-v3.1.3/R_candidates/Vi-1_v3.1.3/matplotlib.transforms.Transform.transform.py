    def transform(self, values):
        """
        Performs the transformation on the given array of values.

        Accepts a numpy array of shape (N x :attr:`input_dims`) and
        returns a numpy array of shape (N x :attr:`output_dims`).

        Alternatively, accepts a numpy array of length :attr:`input_dims`
        and returns a numpy array of length :attr:`output_dims`.
        """
        # Ensure that values is a 2d array (but remember whether
        # we started with a 1d or 2d array).
        values = np.asanyarray(values)
        ndim = values.ndim
        values = values.reshape((-1, self.input_dims))

        # Transform the values
        res = self.transform_affine(self.transform_non_affine(values))

        # Convert the result back to the shape of the input values.
        if ndim == 0:
            assert not np.ma.is_masked(res)  # just to be on the safe side
            return res[0, 0]
        if ndim == 1:
            return res.reshape(-1)
        elif ndim == 2:
            return res
        raise ValueError(
            "Input values must have shape (N x {dims}) "
            "or ({dims}).".format(dims=self.input_dims))
