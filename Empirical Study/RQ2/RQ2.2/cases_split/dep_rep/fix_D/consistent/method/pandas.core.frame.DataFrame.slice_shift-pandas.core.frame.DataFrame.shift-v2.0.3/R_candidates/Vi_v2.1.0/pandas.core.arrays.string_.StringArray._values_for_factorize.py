    def _values_for_factorize(self):
        arr = self._ndarray.copy()
        mask = self.isna()
        arr[mask] = None
        return arr, None
