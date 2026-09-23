    @Appender(_shared_docs["str_split"] % {"side": "end", "method": "rsplit"})
    @forbid_nonstring_types(["bytes"])
    def rsplit(self, pat=None, n=-1, expand=False):
        result = self._data.array._str_rsplit(pat, n=n)
        return self._wrap_result(result, expand=expand, returns_string=expand)
