    @doc(Index._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind):
        assert kind in ["loc", "getitem", None]

        # we will try to coerce to integers
        return self._maybe_cast_indexer(label)
