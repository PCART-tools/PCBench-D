    @Appender(_shared_docs['duplicated'] % _indexops_doc_kwargs)
    def duplicated(self, keep='first'):
        from pandas.core.algorithms import duplicated
        if isinstance(self, ABCIndexClass):
            if self.is_unique:
                return np.zeros(len(self), dtype=np.bool)
            return duplicated(self, keep=keep)
        else:
            return self._constructor(duplicated(self, keep=keep),
                                     index=self.index).__finalize__(self)
