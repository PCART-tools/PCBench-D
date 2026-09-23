    def _str_startswith(self, pat: str, na=None):
        result = pc.starts_with(self._pa_array, pattern=pat)
        if not isna(na):
            result = result.fill_null(na)
        return type(self)(result)
