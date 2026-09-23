    def _maybe_cast_slice_bound(self, label, side: str, kind=lib.no_default):
        self._deprecated_arg(kind, "kind", "_maybe_cast_slice_bound")
        return getattr(self, side)._maybe_cast_slice_bound(label, side)
