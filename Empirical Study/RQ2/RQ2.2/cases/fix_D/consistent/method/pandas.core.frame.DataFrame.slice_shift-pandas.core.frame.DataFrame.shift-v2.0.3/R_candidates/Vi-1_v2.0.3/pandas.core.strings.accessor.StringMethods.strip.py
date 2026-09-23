    @Appender(
        _shared_docs["str_strip"]
        % {
            "side": "left and right sides",
            "method": "strip",
            "position": "leading and trailing",
        }
    )
    @forbid_nonstring_types(["bytes"])
    def strip(self, to_strip=None):
        result = self._data.array._str_strip(to_strip)
        return self._wrap_result(result)
