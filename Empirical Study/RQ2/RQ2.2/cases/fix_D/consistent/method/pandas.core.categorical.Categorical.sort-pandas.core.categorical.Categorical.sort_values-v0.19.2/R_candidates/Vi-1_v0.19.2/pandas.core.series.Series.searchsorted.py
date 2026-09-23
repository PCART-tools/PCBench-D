    @Substitution(klass='Series', value='v')
    @Appender(base._shared_docs['searchsorted'])
    def searchsorted(self, v, side='left', sorter=None):
        if sorter is not None:
            sorter = _ensure_platform_int(sorter)
        return self._values.searchsorted(Series(v)._values,
                                         side=side, sorter=sorter)
