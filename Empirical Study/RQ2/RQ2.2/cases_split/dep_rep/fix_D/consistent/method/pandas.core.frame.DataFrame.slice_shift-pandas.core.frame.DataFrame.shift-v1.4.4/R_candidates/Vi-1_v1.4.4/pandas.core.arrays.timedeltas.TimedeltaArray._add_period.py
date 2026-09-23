    def _add_period(self, other: Period) -> PeriodArray:
        """
        Add a Period object.
        """
        # We will wrap in a PeriodArray and defer to the reversed operation
        from pandas.core.arrays.period import PeriodArray

        i8vals = np.broadcast_to(other.ordinal, self.shape)
        oth = PeriodArray(i8vals, freq=other.freq)
        return oth + self
