    @copy(str_split)
    def split(self, pat=None, n=-1, return_type='series'):
        result = str_split(self.series, pat, n=n, return_type=return_type)
        return self._wrap_result(result)
