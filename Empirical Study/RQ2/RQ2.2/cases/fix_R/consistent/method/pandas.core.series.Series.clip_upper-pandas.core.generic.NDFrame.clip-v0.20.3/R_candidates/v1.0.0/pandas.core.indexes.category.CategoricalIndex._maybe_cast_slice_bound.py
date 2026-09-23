    @Appender(_index_shared_docs["_maybe_cast_slice_bound"])
    def _maybe_cast_slice_bound(self, label, side, kind):
        if kind == "loc":
            return label

        return super()._maybe_cast_slice_bound(label, side, kind)
