    def _str_contains(
        self, pat, case: bool = True, flags: int = 0, na=np.nan, regex: bool = True
    ):
        if flags:
            fallback_performancewarning()
            return super()._str_contains(pat, case, flags, na, regex)

        if regex:
            if case is False:
                fallback_performancewarning()
                return super()._str_contains(pat, case, flags, na, regex)
            else:
                result = pc.match_substring_regex(self._data, pat)
        else:
            if case:
                result = pc.match_substring(self._data, pat)
            else:
                result = pc.match_substring(pc.utf8_upper(self._data), pat.upper())
        result = BooleanDtype().__from_arrow__(result)
        if not isna(na):
            result[isna(result)] = bool(na)
        return result
