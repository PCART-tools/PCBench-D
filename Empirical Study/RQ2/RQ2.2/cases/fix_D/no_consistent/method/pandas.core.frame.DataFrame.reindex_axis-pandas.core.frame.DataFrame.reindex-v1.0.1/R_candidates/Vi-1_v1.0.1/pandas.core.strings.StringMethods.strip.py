    @Appender(
        _shared_docs["str_strip"] % dict(side="left and right sides", method="strip")
    )
    @forbid_nonstring_types(["bytes"])
    def strip(self, to_strip=None):
        result = str_strip(self._parent, to_strip, side="both")
        return self._wrap_result(result)
