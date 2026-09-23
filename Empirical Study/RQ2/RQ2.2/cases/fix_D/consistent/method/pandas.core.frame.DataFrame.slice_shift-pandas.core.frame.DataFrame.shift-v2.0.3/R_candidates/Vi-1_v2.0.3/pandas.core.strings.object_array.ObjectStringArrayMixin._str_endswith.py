    def _str_endswith(self, pat, na=None):
        f = lambda x: x.endswith(pat)
        return self._str_map(f, na_value=na, dtype=np.dtype(bool))
