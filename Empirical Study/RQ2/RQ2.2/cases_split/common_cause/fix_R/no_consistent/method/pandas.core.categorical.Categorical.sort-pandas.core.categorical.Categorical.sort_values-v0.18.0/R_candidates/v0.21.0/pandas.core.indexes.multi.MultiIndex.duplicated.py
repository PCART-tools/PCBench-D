    @Appender(base._shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, keep='first'):
        from pandas.core.sorting import get_group_index
        from pandas._libs.hashtable import duplicated_int64

        shape = map(len, self.levels)
        ids = get_group_index(self.labels, shape, sort=False, xnull=False)

        return duplicated_int64(ids, keep)
