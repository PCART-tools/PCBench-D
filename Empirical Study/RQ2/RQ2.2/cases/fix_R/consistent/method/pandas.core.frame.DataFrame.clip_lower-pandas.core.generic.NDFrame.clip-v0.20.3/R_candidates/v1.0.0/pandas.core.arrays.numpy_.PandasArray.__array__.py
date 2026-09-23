    def __array__(self, dtype=None) -> np.ndarray:
        return np.asarray(self._ndarray, dtype=dtype)
