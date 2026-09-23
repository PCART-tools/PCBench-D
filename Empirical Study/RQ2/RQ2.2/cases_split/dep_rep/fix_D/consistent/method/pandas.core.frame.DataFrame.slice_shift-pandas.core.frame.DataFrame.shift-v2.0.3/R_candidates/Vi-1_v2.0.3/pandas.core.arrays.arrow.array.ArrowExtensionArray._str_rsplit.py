    def _str_rsplit(self, pat: str | None = None, n: int | None = -1):
        if n in {-1, 0}:
            n = None
        return type(self)(pc.split_pattern(self._data, pat, max_splits=n, reverse=True))
