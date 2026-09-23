    def _str_strip(self, to_strip=None):
        if pa_version_under4p0:
            return super()._str_strip(to_strip)

        if to_strip is None:
            result = pc.utf8_trim_whitespace(self._data)
        else:
            result = pc.utf8_trim(self._data, characters=to_strip)
        return type(self)(result)
