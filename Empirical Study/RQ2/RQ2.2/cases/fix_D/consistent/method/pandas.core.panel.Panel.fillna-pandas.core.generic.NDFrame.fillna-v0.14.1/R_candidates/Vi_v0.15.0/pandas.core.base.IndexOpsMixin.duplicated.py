    @Appender(_shared_docs['duplicated'] % _indexops_doc_kwargs)
    def duplicated(self, take_last=False):
        keys = com._ensure_object(self.values)
        duplicated = lib.duplicated(keys, take_last=take_last)
        try:
            return self._constructor(duplicated,
                                     index=self.index).__finalize__(self)
        except AttributeError:
            from pandas.core.index import Index
            return Index(duplicated)
