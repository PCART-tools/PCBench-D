    @copy(str_get)
    def get(self, i):
        result = str_get(self.series, i)
        return self._wrap_result(result)
