    @doc(Index._maybe_cast_slice_bound)
    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
        assert kind in ["loc", "getitem", None, lib.no_default]
        self._deprecated_arg(kind, "kind", "_maybe_cast_slice_bound")

        # we will try to coerce to integers
        return self._maybe_cast_indexer(label)
