    def _str_endswith(self, pat: str, na=None):
        pat = f"{re.escape(pat)}$"
        return self._str_contains(pat, na=na, regex=True)
