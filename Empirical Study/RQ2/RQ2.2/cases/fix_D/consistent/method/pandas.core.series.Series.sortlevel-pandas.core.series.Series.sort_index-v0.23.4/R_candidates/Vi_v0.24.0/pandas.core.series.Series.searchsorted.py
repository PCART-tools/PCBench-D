    @Substitution(klass='Series')
    @Appender(base._shared_docs['searchsorted'])
    def searchsorted(self, value, side='left', sorter=None):
        if sorter is not None:
            sorter = ensure_platform_int(sorter)
        result = self._values.searchsorted(Series(value)._values,
                                           side=side, sorter=sorter)

        return result[0] if is_scalar(value) else result
