    @copy(str_match)
    def match(self, pat, case=True, flags=0, na=np.nan, as_indexer=False):
        result = str_match(self.series, pat, case=case, flags=flags,
                              na=na, as_indexer=as_indexer)
        return self._wrap_result(result)
