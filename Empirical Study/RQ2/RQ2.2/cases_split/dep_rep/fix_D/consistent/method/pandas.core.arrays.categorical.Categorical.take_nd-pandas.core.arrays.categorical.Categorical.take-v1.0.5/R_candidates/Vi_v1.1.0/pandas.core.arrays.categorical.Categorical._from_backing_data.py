    def _from_backing_data(self, arr: np.ndarray) -> "Categorical":
        return self._constructor(arr, dtype=self.dtype, fastpath=True)
