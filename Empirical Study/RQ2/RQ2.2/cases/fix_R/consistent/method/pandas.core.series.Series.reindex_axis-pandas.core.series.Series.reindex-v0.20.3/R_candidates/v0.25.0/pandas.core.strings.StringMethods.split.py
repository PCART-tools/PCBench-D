    @Appender(_shared_docs["str_split"] % {"side": "beginning", "method": "split"})
    @forbid_nonstring_types(["bytes"])
    def split(self, pat=None, n=-1, expand=False):
        result = str_split(self._parent, pat, n=n)
        return self._wrap_result(result, expand=expand)
