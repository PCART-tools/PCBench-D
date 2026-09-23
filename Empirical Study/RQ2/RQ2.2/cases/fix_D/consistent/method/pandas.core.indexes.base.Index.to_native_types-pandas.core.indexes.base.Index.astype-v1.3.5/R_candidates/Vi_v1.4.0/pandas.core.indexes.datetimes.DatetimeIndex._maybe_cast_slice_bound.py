    @doc(DatetimeTimedeltaMixin._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
        label = super()._maybe_cast_slice_bound(label, side, kind=kind)
        self._deprecate_mismatched_indexing(label)
        return self._maybe_cast_for_get_loc(label)
