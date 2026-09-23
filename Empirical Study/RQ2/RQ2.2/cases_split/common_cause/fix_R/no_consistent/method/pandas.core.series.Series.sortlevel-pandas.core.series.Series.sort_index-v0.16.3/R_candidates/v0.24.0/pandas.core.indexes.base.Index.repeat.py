    @Appender(_index_shared_docs['repeat'] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        return self._shallow_copy(self._values.repeat(repeats))
