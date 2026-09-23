    @doc(Index.get_slice_bound)
    def get_slice_bound(
        self, label, side: Literal["left", "right"], kind=lib.no_default
    ) -> int:
        # GH#42855 handle date here instead of _maybe_cast_slice_bound
        if isinstance(label, date) and not isinstance(label, datetime):
            label = Timestamp(label).to_pydatetime()
        return super().get_slice_bound(label, side=side, kind=kind)
