    def union(self, other):
        """
        Specialized union for DatetimeIndex objects. If combine
        overlapping ranges with the same DateOffset, will be much
        faster than Index.union

        Parameters
        ----------
        other : DatetimeIndex or array-like

        Returns
        -------
        y : Index or DatetimeIndex
        """
        self._assert_can_do_setop(other)
        if not isinstance(other, DatetimeIndex):
            try:
                other = DatetimeIndex(other)
            except TypeError:
                pass

        this, other = self._maybe_utc_convert(other)

        if this._can_fast_union(other):
            return this._fast_union(other)
        else:
            result = Index.union(this, other)
            if isinstance(result, DatetimeIndex):
                result._tz = timezones.tz_standardize(this.tz)
                if (result.freq is None and
                        (this.freq is not None or other.freq is not None)):
                    result.freq = to_offset(result.inferred_freq)
            return result
