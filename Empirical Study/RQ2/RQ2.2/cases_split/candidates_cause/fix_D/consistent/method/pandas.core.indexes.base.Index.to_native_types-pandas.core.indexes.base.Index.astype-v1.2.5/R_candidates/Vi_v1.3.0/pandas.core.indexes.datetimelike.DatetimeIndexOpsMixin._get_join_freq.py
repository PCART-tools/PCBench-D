    def _get_join_freq(self, other):
        """
        Get the freq to attach to the result of a join operation.
        """
        if is_period_dtype(self.dtype):
            freq = self.freq
        else:
            self = cast(DatetimeTimedeltaMixin, self)
            freq = self.freq if self._can_fast_union(other) else None
        return freq
