    def _add_period(self, other: Period):
        """
        Add a Period object.
        """
        # We will wrap in a PeriodArray and defer to the reversed operation
        from .period import PeriodArray

        i8vals = np.broadcast_to(other.ordinal, self.shape)
        oth = PeriodArray(i8vals, freq=other.freq)
        return oth + self
