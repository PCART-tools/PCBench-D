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
            fallback_performancewarning()
            return super()._str_replace(pat, repl, n, case, flags, regex)

        func = pc.replace_substring_regex if regex else pc.replace_substring
        result = func(self._pa_array, pattern=pat, replacement=repl, max_replacements=n)
        return type(self)(result)
