    def _str_contains(
        self, pat, case: bool = True, flags: int = 0, na=np.nan, regex: bool = True
    ):
        if flags:
            fallback_performancewarning()
            return super()._str_contains(pat, case, flags, na, regex)

        if regex:
            result = pc.match_substring_regex(self._pa_array, pat, ignore_case=not case)
        else:
            result = pc.match_substring(self._pa_array, pat, ignore_case=not case)
        result = self._result_converter(result, na=na)
        if not isna(na):
            result[isna(result)] = bool(na)
        return result
