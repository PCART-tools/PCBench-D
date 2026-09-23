    def __array__(self, dtype=None):
        """
        The array interface, return my values.
        """
        return np.asarray(self._data, dtype=dtype)
