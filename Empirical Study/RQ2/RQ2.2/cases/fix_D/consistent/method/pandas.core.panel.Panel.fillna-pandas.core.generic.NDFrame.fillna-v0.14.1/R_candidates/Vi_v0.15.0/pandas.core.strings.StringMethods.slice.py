    @copy(str_slice)
    def slice(self, start=None, stop=None, step=1):
        result = str_slice(self.series, start, stop)
        return self._wrap_result(result)
