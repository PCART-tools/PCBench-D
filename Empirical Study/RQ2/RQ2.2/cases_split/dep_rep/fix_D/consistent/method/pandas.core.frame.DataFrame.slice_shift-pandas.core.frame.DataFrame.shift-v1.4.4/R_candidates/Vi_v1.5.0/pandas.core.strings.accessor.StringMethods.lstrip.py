    @Appender(
        _shared_docs["str_strip"]
        % {"side": "left side", "method": "lstrip", "position": "leading"}
    )
    @forbid_nonstring_types(["bytes"])
    def lstrip(self, to_strip=None):
        result = self._data.array._str_lstrip(to_strip)
        return self._wrap_result(result)
