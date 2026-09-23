    @copy(str_contains)
    def contains(self, pat, case=True, flags=0, na=np.nan, regex=True):
        result = str_contains(self.series, pat, case=case, flags=flags,
                              na=na, regex=regex)
        return self._wrap_result(result)
