    @Appender(_shared_docs["str_split"] % {"side": "end", "method": "rsplit"})
    @forbid_nonstring_types(["bytes"])
    def rsplit(self, pat=None, n=-1, expand=False):
        result = str_rsplit(self._parent, pat, n=n)
        return self._wrap_result(result, expand=expand, returns_string=expand)
