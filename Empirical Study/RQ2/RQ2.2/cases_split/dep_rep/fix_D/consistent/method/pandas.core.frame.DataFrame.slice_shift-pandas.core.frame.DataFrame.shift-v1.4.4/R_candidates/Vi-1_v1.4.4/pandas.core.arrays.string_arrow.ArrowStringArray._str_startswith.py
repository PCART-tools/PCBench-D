    def _str_startswith(self, pat: str, na=None):
        if pa_version_under4p0:
            return super()._str_startswith(pat, na)

        pat = "^" + re.escape(pat)
        return self._str_contains(pat, na=na, regex=True)
