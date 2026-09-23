    def _str_startswith(self, pat, na=None):
        f = lambda x: x.startswith(pat)
        return self._str_map(f, na_value=na, dtype=np.dtype(bool))
