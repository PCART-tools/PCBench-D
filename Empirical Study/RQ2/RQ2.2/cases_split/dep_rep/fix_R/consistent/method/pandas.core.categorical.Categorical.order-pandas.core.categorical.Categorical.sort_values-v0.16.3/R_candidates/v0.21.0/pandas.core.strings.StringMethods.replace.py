    @copy(str_replace)
    def replace(self, pat, repl, n=-1, case=None, flags=0):
        result = str_replace(self._data, pat, repl, n=n, case=case,
                             flags=flags)
        return self._wrap_result(result)
