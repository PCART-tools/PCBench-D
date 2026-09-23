    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        nv.validate_take(tuple(), kwargs)
        indices = ensure_int64(indices)

        maybe_slice = lib.maybe_indices_to_slice(indices, len(self))
        if isinstance(maybe_slice, slice):
            return self[maybe_slice]

        taken = self._assert_take_fillable(
            self.asi8,
            indices,
            allow_fill=allow_fill,
            fill_value=fill_value,
            na_value=iNaT,
        )

        # keep freq in PeriodArray/Index, reset otherwise
        freq = self.freq if is_period_dtype(self) else None
        return self._shallow_copy(taken, freq=freq)
