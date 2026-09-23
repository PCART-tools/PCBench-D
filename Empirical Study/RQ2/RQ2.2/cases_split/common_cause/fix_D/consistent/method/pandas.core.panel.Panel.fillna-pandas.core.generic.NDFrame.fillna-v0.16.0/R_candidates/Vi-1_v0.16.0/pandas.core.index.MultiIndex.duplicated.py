    @Appender(_shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, take_last=False):
        from pandas.core.groupby import get_group_index
        from pandas.hashtable import duplicated_int64

        shape = map(len, self.levels)
        ids = get_group_index(self.labels, shape, sort=False, xnull=False)

        return duplicated_int64(ids, take_last)
