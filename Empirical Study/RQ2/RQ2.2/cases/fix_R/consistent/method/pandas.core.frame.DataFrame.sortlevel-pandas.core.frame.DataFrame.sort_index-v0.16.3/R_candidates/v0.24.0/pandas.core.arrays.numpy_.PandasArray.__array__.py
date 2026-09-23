    def __array__(self, dtype=None):
        return np.asarray(self._ndarray, dtype=dtype)
