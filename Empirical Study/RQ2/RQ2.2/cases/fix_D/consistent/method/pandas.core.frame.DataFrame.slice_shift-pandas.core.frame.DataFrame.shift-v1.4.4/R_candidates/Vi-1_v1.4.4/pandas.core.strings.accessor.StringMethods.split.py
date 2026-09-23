    @Appender(_shared_docs["str_split"] % {"side": "beginning", "method": "split"})
    @forbid_nonstring_types(["bytes"])
    def split(
        self,
        pat: str | re.Pattern | None = None,
        n=-1,
        expand=False,
        *,
        regex: bool | None = None,
    ):
        if regex is False and is_re(pat):
            raise ValueError(
                "Cannot use a compiled regex as replacement pattern with regex=False"
            )
        if is_re(pat):
            regex = True
        result = self._data.array._str_split(pat, n, expand, regex)
        return self._wrap_result(result, returns_string=expand, expand=expand)
