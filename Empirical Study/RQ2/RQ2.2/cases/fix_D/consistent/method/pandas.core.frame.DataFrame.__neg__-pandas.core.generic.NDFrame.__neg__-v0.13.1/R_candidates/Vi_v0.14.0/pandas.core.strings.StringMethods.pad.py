    @copy(str_pad)
    def pad(self, width, side='left'):
        result = str_pad(self.series, width, side=side)
        return self._wrap_result(result)
