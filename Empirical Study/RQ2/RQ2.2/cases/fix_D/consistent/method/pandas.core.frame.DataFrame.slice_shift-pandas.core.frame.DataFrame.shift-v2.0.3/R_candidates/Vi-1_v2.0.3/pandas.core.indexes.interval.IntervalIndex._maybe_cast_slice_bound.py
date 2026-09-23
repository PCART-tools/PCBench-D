    def _maybe_cast_slice_bound(self, label, side: str):
        return getattr(self, side)._maybe_cast_slice_bound(label, side)
