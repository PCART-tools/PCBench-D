    def __array__(self, dtype: npt.DTypeLike | None = None) -> np.ndarray:
        return np.asarray(self._values, dtype=dtype)
