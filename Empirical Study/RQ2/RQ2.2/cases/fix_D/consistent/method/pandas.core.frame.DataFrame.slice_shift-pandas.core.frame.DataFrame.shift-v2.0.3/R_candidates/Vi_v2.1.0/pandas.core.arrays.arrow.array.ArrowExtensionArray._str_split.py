    def _str_split(
        self,
        pat: str | None = None,
        n: int | None = -1,
        expand: bool = False,
        regex: bool | None = None,
    ):
        if n in {-1, 0}:
            n = None
        if regex:
            split_func = pc.split_pattern_regex
        else:
            split_func = pc.split_pattern
        return type(self)(split_func(self._pa_array, pat, max_splits=n))
