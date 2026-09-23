    def _values_for_factorize(self):
        # int64 instead of int ensures we have a "view" method
        return self._ndarray, np.int64(iNaT)
