    @copy(str_wrap)
    def wrap(self, width, **kwargs):
        result = str_wrap(self.series, width, **kwargs)
        return self._wrap_result(result)
