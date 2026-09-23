    @copy(str_split)
    def split(self, pat=None, n=-1, expand=False):
        result = str_split(self._data, pat, n=n)
        return self._wrap_result(result, expand=expand)
