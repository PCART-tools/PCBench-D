    @Appender(
        _shared_docs["str_removefix"] % {"side": "prefix", "other_side": "suffix"}
    )
    @forbid_nonstring_types(["bytes"])
    def removeprefix(self, prefix):
        result = self._data.array._str_removeprefix(prefix)
        return self._wrap_result(result)
