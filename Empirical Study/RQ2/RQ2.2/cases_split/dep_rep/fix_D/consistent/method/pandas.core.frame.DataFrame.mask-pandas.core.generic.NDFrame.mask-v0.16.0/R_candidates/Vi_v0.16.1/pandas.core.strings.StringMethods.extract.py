    @copy(str_extract)
    def extract(self, pat, flags=0):
        result, name = str_extract(self.series, pat, flags=flags)
        return self._wrap_result(result, name=name)
