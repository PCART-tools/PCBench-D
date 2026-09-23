    def _addsub_int_array(self, other, op):
        """
        Add or subtract array-like of integers equivalent to applying
        `_time_shift` pointwise.

        Parameters
        ----------
        other : Index, ExtensionArray, np.ndarray
            integer-dtype
        op : {operator.add, operator.sub}

        Returns
        -------
        result : same class as self
        """
        # _addsub_int_array is overriden by PeriodArray
        assert not is_period_dtype(self)
        assert op in [operator.add, operator.sub]

        if self.freq is None:
            # GH#19123
            raise NullFrequencyError("Cannot shift with no freq")

        elif isinstance(self.freq, Tick):
            # easy case where we can convert to timedelta64 operation
            td = Timedelta(self.freq)
            return op(self, td * other)

        # We should only get here with DatetimeIndex; dispatch
        # to _addsub_offset_array
        assert not is_timedelta64_dtype(self)
        return op(self, np.array(other) * self.freq)
