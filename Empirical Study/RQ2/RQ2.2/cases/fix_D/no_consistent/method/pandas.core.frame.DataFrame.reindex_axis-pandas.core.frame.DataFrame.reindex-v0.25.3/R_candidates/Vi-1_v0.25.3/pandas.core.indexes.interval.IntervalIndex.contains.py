    @Appender(_interval_shared_docs["contains"] % _index_doc_kwargs)
    def contains(self, other):
        return self._data.contains(other)
