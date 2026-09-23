    @copy(str_slice)
    def slice(self, start=None, stop=None, step=None):
        result = str_slice(self.series, start, stop, step)
        return self._wrap_result(result)
