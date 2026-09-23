    def _str_rstrip(self, to_strip=None):
        if to_strip is None:
            result = pc.utf8_rtrim_whitespace(self._data)
        else:
            result = pc.utf8_rtrim(self._data, characters=to_strip)
        return type(self)(result)
