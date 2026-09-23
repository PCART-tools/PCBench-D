    @Appender(
        _shared_docs["str_removefix"] % {"side": "suffix", "other_side": "prefix"}
    )
    @forbid_nonstring_types(["bytes"])
    def removesuffix(self, suffix):
        result = self._data.array._str_removesuffix(suffix)
        return self._wrap_result(result)
