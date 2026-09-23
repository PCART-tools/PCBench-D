    def _str_endswith(self, pat: str, na=None):
        result = pc.ends_with(self._pa_array, pattern=pat)
        if not isna(na):
            result = result.fill_null(na)
        return type(self)(result)
