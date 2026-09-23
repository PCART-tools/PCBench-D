    @doc(DatetimeTimedeltaMixin._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):

        # GH#42855 handle date here instead of get_slice_bound
        if isinstance(label, date) and not isinstance(label, datetime):
            # Pandas supports slicing with dates, treated as datetimes at midnight.
            # https://github.com/pandas-dev/pandas/issues/31501
            label = Timestamp(label).to_pydatetime()

        label = super()._maybe_cast_slice_bound(label, side, kind=kind)
        self._deprecate_mismatched_indexing(label)
        return self._maybe_cast_for_get_loc(label)
