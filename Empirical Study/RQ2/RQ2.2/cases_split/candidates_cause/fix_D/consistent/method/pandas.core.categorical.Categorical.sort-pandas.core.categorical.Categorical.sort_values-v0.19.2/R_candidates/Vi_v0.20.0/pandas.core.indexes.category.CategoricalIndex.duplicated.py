    @Appender(base._shared_docs['duplicated'] % _index_doc_kwargs)
    def duplicated(self, keep='first'):
        from pandas._libs.hashtable import duplicated_int64
        codes = self.codes.astype('i8')
        return duplicated_int64(codes, keep)
