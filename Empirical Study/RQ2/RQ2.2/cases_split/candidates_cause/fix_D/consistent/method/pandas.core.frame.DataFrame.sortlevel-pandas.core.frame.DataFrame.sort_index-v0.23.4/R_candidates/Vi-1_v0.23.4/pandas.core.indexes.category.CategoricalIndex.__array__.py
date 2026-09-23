    def __array__(self, dtype=None):
        """ the array interface, return my values """
        return np.array(self._data, dtype=dtype)
