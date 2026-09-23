    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        if kwargs:
            nv.validate_take((), kwargs)
        indices = ensure_platform_int(indices)
        allow_fill = self._maybe_disallow_fill(allow_fill, fill_value, indices)

        # Note: we discard fill_value and use self._na_value, only relevant
        #  in the case where allow_fill is True and fill_value is not None
        taken = algos.take(
            self._values, indices, allow_fill=allow_fill, fill_value=self._na_value
        )
        return self._shallow_copy(taken)
