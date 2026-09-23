    def __array__(self, dtype=None) -> np.ndarray:
        """ the array interface, return my values """
        return np.array(self._data, dtype=dtype)
