    def __array__(self, dtype: NpDtype | None = None) -> np.ndarray:
        return np.asarray(self._ndarray, dtype=dtype)
