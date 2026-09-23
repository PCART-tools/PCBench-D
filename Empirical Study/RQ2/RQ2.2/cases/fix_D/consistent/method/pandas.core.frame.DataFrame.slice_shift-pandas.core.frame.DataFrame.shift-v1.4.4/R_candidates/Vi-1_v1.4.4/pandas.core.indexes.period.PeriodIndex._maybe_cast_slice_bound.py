    @doc(DatetimeIndexOpsMixin._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
        if isinstance(label, datetime):
            label = Period(label, freq=self.freq)

        return super()._maybe_cast_slice_bound(label, side, kind=kind)
