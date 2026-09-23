    def _maybe_promote(self, other):
        if other.inferred_type == "date":
            other = DatetimeIndex(other)
        return self, other
