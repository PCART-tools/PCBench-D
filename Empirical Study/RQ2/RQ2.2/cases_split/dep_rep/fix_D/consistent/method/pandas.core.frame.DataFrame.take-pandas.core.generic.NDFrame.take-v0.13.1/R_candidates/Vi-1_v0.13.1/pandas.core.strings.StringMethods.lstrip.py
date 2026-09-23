    @copy(str_lstrip)
    def lstrip(self, to_strip=None):
        result = str_lstrip(self.series, to_strip)
        return self._wrap_result(result)
