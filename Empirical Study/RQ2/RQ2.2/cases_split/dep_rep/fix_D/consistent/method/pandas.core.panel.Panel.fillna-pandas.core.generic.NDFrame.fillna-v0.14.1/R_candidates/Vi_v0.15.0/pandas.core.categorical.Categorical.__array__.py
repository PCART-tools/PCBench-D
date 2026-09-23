    def __array__(self, dtype=None):
        """ The numpy array interface.

        Returns
        -------
        values : numpy array
            A numpy array of either the specified dtype or, if dtype==None (default), the same
            dtype as categorical.categories.dtype
        """
        ret = com.take_1d(self.categories.values, self._codes)
        if dtype and dtype != self.categories.dtype:
            return np.asarray(ret, dtype)
        return ret
