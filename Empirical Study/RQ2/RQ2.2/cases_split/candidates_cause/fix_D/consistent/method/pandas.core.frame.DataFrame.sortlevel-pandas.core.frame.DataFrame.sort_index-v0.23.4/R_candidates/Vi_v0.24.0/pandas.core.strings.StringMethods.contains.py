    @copy(str_contains)
    def contains(self, pat, case=True, flags=0, na=np.nan, regex=True):
        result = str_contains(self._parent, pat, case=case, flags=flags, na=na,
                              regex=regex)
        return self._wrap_result(result, fill_value=na)
