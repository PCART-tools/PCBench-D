    @Appender(_shared_docs['str_partition'] % {'side': 'first',
        'return': '3 elements containing the string itself, followed by two empty strings',
        'also': 'rpartition : Split the string at the last occurrence of `sep`'})
    def partition(self, pat=' ', expand=True):
        f = lambda x: x.partition(pat)
        result = _na_map(f, self.series)
        return self._wrap_result_expand(result, expand=expand)
