    def _maybe_cast_slice_bound(self, label, side, kind):
        return getattr(self, side)._maybe_cast_slice_bound(label, side, kind)
