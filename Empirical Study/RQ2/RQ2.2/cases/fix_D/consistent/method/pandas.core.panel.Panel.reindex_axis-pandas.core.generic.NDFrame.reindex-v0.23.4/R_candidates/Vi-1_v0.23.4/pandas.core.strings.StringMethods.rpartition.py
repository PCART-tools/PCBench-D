    @Appender(_shared_docs['str_partition'] % {
        'side': 'last',
        'return': '3 elements containing two empty strings, followed by the '
                  'string itself',
        'also': 'partition : Split the string at the first occurrence of `sep`'
    })
    def rpartition(self, pat=' ', expand=True):
        f = lambda x: x.rpartition(pat)
        result = _na_map(f, self._data)
        return self._wrap_result(result, expand=expand)
