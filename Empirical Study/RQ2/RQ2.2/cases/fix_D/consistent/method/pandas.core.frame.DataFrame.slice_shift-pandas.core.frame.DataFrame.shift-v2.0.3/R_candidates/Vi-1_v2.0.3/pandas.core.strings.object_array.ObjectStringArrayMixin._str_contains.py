    def _str_contains(
        self, pat, case: bool = True, flags: int = 0, na=np.nan, regex: bool = True
    ):
        if regex:
            if not case:
                flags |= re.IGNORECASE

            pat = re.compile(pat, flags=flags)

            f = lambda x: pat.search(x) is not None
        else:
            if case:
                f = lambda x: pat in x
            else:
                upper_pat = pat.upper()
                f = lambda x: upper_pat in x.upper()
        return self._str_map(f, na, dtype=np.dtype("bool"))
