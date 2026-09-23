    @copy(str_join)
    def join(self, sep):
        result = str_join(self.series, sep)
        return self._wrap_result(result)
