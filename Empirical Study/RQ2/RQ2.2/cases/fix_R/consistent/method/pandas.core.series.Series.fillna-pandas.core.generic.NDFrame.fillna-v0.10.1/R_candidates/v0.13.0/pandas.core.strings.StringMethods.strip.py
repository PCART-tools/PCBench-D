    @copy(str_strip)
    def strip(self, to_strip=None):
        result = str_strip(self.series, to_strip)
        return self._wrap_result(result)
