    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return other in [self.name, self.name.title()]

        elif isinstance(other, PeriodDtype):
            # For freqs that can be held by a PeriodDtype, this check is
            # equivalent to (and much faster than) self.freq == other.freq
            sfreq = self.freq
            ofreq = other.freq
            return (
                sfreq.n == ofreq.n
                and sfreq._period_dtype_code == ofreq._period_dtype_code
            )

        return False
