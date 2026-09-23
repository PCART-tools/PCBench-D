    @doc(Index._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind):
        if kind == "loc":
            return label

        return super()._maybe_cast_slice_bound(label, side, kind)
