    @copy(str_rstrip)
    def rstrip(self, to_strip=None):
        result = str_rstrip(self.series, to_strip)
        return self._wrap_result(result)
