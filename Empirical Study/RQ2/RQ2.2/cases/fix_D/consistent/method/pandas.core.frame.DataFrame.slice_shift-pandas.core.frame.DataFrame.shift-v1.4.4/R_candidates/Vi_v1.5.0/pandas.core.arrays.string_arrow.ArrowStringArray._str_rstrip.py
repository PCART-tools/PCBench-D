    def _str_rstrip(self, to_strip=None):
        if pa_version_under4p0:
            fallback_performancewarning(version="4")
            return super()._str_rstrip(to_strip)

        if to_strip is None:
            result = pc.utf8_rtrim_whitespace(self._data)
        else:
            result = pc.utf8_rtrim(self._data, characters=to_strip)
        return type(self)(result)
