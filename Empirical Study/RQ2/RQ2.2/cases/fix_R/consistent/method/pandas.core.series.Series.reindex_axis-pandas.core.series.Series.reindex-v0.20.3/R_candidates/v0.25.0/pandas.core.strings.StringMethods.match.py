    @copy(str_match)
    @forbid_nonstring_types(["bytes"])
    def match(self, pat, case=True, flags=0, na=np.nan):
        result = str_match(self._parent, pat, case=case, flags=flags, na=na)
        return self._wrap_result(result, fill_value=na)
