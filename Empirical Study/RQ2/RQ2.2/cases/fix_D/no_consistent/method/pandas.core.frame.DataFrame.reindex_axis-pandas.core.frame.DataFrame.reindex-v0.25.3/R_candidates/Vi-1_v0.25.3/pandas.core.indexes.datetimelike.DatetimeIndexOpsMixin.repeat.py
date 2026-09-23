    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        freq = self.freq if is_period_dtype(self) else None
        return self._shallow_copy(self.asi8.repeat(repeats), freq=freq)
