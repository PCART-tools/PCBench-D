    @deprecate_kwarg('return_type', 'expand',
                     mapping={'series': False, 'frame': True})
    @copy(str_split)
    def split(self, pat=None, n=-1, expand=False):
        result = str_split(self.series, pat, n=n)
        return self._wrap_result_expand(result, expand=expand)
