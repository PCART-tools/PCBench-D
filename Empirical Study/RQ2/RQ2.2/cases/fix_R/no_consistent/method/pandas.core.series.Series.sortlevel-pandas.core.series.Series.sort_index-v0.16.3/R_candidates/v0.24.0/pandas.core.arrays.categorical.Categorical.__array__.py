    def __array__(self, dtype=None):
        """
        The numpy array interface.

        Returns
        -------
        values : numpy array
            A numpy array of either the specified dtype or,
            if dtype==None (default), the same dtype as
            categorical.categories.dtype
        """
        ret = take_1d(self.categories.values, self._codes)
        if dtype and not is_dtype_equal(dtype, self.categories.dtype):
            return np.asarray(ret, dtype)
        if is_extension_array_dtype(ret):
            # When we're a Categorical[ExtensionArray], like Interval,
            # we need to ensure __array__ get's all the way to an
            # ndarray.
            ret = np.asarray(ret)
        return ret
