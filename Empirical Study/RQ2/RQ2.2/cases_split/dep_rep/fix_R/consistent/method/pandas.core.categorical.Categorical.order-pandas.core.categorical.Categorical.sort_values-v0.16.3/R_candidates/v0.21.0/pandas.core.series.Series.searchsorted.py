    @Substitution(klass='Series')
    @Appender(base._shared_docs['searchsorted'])
    @deprecate_kwarg(old_arg_name='v', new_arg_name='value')
    def searchsorted(self, value, side='left', sorter=None):
        if sorter is not None:
            sorter = _ensure_platform_int(sorter)
        return self._values.searchsorted(Series(value)._values,
                                         side=side, sorter=sorter)
