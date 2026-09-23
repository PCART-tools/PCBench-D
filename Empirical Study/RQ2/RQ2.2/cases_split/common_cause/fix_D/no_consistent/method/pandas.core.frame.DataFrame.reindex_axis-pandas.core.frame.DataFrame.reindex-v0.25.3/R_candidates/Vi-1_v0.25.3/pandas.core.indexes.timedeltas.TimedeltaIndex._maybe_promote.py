    def _maybe_promote(self, other):
        if other.inferred_type == "timedelta":
            other = TimedeltaIndex(other)
        return self, other
