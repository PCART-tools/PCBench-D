    def _str_match(
        self, pat: str, case: bool = True, flags: int = 0, na: Scalar | None = None
    ):
        if pa_version_under4p0:
            fallback_performancewarning(version="4")
            return super()._str_match(pat, case, flags, na)

        if not pat.startswith("^"):
            pat = "^" + pat
        return self._str_contains(pat, case, flags, na, regex=True)
