    @Appender(
        _shared_docs["str_partition"]
        % {
            "side": "last",
            "return": "3 elements containing two empty strings, followed by the "
            "string itself",
            "also": "partition : Split the string at the first occurrence of `sep`.",
        }
    )
    @forbid_nonstring_types(["bytes"])
    def rpartition(self, sep=" ", expand=True):
        f = lambda x: x.rpartition(sep)
        result = _na_map(f, self._parent)
        return self._wrap_result(result, expand=expand, returns_string=expand)
