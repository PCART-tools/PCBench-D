    def _str_replace(
        self,
        pat: str | re.Pattern,
        repl: str | Callable,
        n: int = -1,
        case: bool = True,
        flags: int = 0,
        regex: bool = True,
    ):
        if isinstance(pat, re.Pattern) or callable(repl) or not case or flags:
            raise NotImplementedError(
                "replace is not supported with a re.Pattern, callable repl, "
                "case=False, or flags!=0"
            )

        func = pc.replace_substring_regex if regex else pc.replace_substring
        result = func(self._data, pattern=pat, replacement=repl, max_replacements=n)
        return type(self)(result)
