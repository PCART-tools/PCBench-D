    def _str_fullmatch(self, pat, case: bool = True, flags: int = 0, na: Scalar = None):
        if pa_version_under4p0:
            return super()._str_fullmatch(pat, case, flags, na)

        if not pat.endswith("$") or pat.endswith("//$"):
            pat = pat + "$"
        return self._str_match(pat, case, flags, na)
