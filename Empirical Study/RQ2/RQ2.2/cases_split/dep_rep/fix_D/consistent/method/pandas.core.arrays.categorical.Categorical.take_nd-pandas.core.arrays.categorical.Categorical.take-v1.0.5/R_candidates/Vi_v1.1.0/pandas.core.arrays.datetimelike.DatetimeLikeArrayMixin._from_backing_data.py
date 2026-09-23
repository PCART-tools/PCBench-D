    def _from_backing_data(self: _T, arr: np.ndarray) -> _T:
        # Note: we do not retain `freq`
        return type(self)(arr, dtype=self.dtype)  # type: ignore
