    @copy(str_rsplit)
    def rsplit(self, pat=None, n=-1, expand=False):
        result = str_rsplit(self._data, pat, n=n)
        return self._wrap_result(result, expand=expand)
