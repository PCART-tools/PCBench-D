    @Appender(
        _shared_docs["str_strip"]
        % {"side": "right side", "method": "rstrip", "position": "trailing"}
    )
    @forbid_nonstring_types(["bytes"])
    def rstrip(self, to_strip=None):
        result = self._data.array._str_rstrip(to_strip)
        return self._wrap_result(result)
