    def _ensure_matching_resos(self, other):
        if self._creso != other._creso:
            # Just as with Timestamp/Timedelta, we cast to the higher resolution
            if self._creso < other._creso:
                self = self.as_unit(other.unit)
            else:
                other = other.as_unit(self.unit)
        return self, other
