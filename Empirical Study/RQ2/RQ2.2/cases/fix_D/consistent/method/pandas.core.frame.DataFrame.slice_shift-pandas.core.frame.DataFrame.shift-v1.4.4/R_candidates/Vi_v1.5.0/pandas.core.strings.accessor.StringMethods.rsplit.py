    @Appender(
        _shared_docs["str_split"]
        % {
            "side": "end",
            "pat_regex": "",
            "pat_description": "String to split on",
            "regex_argument": "",
            "raises_split": "",
            "regex_pat_note": "",
            "method": "rsplit",
            "regex_examples": "",
        }
    )
    @deprecate_nonkeyword_arguments(version=None, allowed_args=["self", "pat"])
    @forbid_nonstring_types(["bytes"])
    def rsplit(self, pat=None, n=-1, expand=False):
        result = self._data.array._str_rsplit(pat, n=n)
        return self._wrap_result(result, expand=expand, returns_string=expand)
