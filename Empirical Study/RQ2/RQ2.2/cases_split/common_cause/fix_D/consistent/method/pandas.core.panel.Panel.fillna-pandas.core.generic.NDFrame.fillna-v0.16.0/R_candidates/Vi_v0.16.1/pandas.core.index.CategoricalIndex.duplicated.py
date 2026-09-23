    @Appender(_shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, take_last=False):
        from pandas.hashtable import duplicated_int64
        return duplicated_int64(self.codes.astype('i8'), take_last)
