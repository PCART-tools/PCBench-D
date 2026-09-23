    @Appender(
        _shared_docs["str_partition"]
        % {
            "side": "first",
            "return": "3 elements containing the string itself, followed by two "
            "empty strings",
            "also": "rpartition : Split the string at the last occurrence of `sep`.",
        }
    )
    @forbid_nonstring_types(["bytes"])
    def partition(self, sep=" ", expand=True):
        f = lambda x: x.partition(sep)
        result = _na_map(f, self._parent)
        return self._wrap_result(result, expand=expand, returns_string=expand)
