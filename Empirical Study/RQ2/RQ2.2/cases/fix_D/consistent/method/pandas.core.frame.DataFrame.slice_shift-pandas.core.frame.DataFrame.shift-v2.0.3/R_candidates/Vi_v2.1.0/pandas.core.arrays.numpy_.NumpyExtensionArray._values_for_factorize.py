    def _values_for_factorize(self) -> tuple[np.ndarray, float | None]:
        if self.dtype.kind in "iub":
            fv = None
        else:
            fv = np.nan
        return self._ndarray, fv
