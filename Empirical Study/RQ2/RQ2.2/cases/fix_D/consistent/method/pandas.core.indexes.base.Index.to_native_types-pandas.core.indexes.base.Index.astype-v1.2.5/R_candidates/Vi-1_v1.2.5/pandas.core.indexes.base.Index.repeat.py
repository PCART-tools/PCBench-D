    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        repeats = ensure_platform_int(repeats)
        nv.validate_repeat((), {"axis": axis})
        return self._shallow_copy(self._values.repeat(repeats))
