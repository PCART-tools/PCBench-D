    @ravel_compat
    def __array__(self, dtype: NpDtype | None = None) -> np.ndarray:
        """
        The numpy array interface.

        Returns
        -------
        numpy.array
            A numpy array of either the specified dtype or,
            if dtype==None (default), the same dtype as
            categorical.categories.dtype.
        """
        ret = take_nd(self.categories._values, self._codes)
        if dtype and not is_dtype_equal(dtype, self.categories.dtype):
            return np.asarray(ret, dtype)
        # When we're a Categorical[ExtensionArray], like Interval,
        # we need to ensure __array__ gets all the way to an
        # ndarray.
        return np.asarray(ret)
