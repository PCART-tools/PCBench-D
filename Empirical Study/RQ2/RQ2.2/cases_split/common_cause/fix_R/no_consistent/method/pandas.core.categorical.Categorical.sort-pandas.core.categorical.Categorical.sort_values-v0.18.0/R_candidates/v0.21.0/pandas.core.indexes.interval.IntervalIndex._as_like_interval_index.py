    def _as_like_interval_index(self, other, error_msg):
        self._assert_can_do_setop(other)
        other = _ensure_index(other)
        if (not isinstance(other, IntervalIndex) or
                self.closed != other.closed):
            raise ValueError(error_msg)
        return other
