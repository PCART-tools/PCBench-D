    @copy(str_replace)
    def replace(self, pat, repl, n=-1, case=True, flags=0):
        result = str_replace(self.series, pat, repl, n=n, case=case,
                             flags=flags)
        return self._wrap_result(result)
