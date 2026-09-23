    @Appender(_interval_shared_docs['overlaps'] % _index_doc_kwargs)
    def overlaps(self, other):
        return self._data.overlaps(other)
