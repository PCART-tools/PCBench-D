    @Appender(_shared_docs['str_partition'] % {
        'side': 'last',
        'return': '3 elements containing two empty strings, followed by the '
                  'string itself',
        'also': 'partition : Split the string at the first occurrence of '
                '`sep`.'
    })
    @deprecate_kwarg(old_arg_name='pat', new_arg_name='sep')
    def rpartition(self, sep=' ', expand=True):
        f = lambda x: x.rpartition(sep)
        result = _na_map(f, self._parent)
        return self._wrap_result(result, expand=expand)
