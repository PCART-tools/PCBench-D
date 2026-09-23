    def _str_removesuffix(self, suffix: str):
        ends_with = pc.ends_with(self._data, pattern=suffix)
        removed = pc.utf8_slice_codeunits(self._data, 0, stop=-len(suffix))
        result = pc.if_else(ends_with, removed, self._data)
        return type(self)(result)
