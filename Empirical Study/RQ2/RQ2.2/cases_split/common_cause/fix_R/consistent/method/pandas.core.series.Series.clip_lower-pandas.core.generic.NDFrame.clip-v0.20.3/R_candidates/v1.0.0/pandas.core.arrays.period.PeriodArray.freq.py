    @property  # type: ignore
    def freq(self):
        """
        Return the frequency object for this PeriodArray.
        """
        return self.dtype.freq
