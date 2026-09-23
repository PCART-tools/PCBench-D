    def _require_matching_freq(self, other, base: bool = False) -> None:
        # See also arrays.period.raise_on_incompatible
        if isinstance(other, BaseOffset):
            other_freq = other
        else:
            other_freq = other.freq

        if base:
            condition = self.freq.base != other_freq.base
        else:
            condition = self.freq != other_freq

        if condition:
            msg = DIFFERENT_FREQ.format(
                cls=type(self).__name__,
                own_freq=self.freqstr,
                other_freq=other_freq.freqstr,
            )
            raise IncompatibleFrequency(msg)
