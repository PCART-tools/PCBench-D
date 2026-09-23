    @copy(str_split)
    def split(self, pat=None, n=-1):
        result = str_split(self.series, pat, n=n)
        return self._wrap_result(result)
