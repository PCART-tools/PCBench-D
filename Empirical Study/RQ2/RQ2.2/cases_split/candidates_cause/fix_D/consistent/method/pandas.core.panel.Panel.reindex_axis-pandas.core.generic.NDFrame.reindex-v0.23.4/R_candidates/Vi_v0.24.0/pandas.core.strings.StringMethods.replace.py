    @copy(str_replace)
    def replace(self, pat, repl, n=-1, case=None, flags=0, regex=True):
        result = str_replace(self._parent, pat, repl, n=n, case=case,
                             flags=flags, regex=regex)
        return self._wrap_result(result)
