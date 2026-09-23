    def _assert_can_do_setop(self, other):
        super()._assert_can_do_setop(other)

        # *Can't* use PeriodIndexes of different freqs
        # *Can* use PeriodIndex/DatetimeIndex
        if isinstance(other, PeriodIndex) and self.freq != other.freq:
            raise raise_on_incompatible(self, other)
