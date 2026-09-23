    def union(self, other):
        """
        Specialized union for TimedeltaIndex objects. If combine
        overlapping ranges with the same DateOffset, will be much
        faster than Index.union

        Parameters
        ----------
        other : TimedeltaIndex or array-like

        Returns
        -------
        y : Index or TimedeltaIndex
        """
        self._assert_can_do_setop(other)

        if len(other) == 0 or self.equals(other) or len(self) == 0:
            return super(TimedeltaIndex, self).union(other)

        if not isinstance(other, TimedeltaIndex):
            try:
                other = TimedeltaIndex(other)
            except (TypeError, ValueError):
                pass
        this, other = self, other

        if this._can_fast_union(other):
            return this._fast_union(other)
        else:
            result = Index.union(this, other)
            if isinstance(result, TimedeltaIndex):
                if result.freq is None:
                    result.freq = to_offset(result.inferred_freq)
            return result
