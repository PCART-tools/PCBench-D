    def _assert_can_do_setop(self, other):
        super(PeriodIndex, self)._assert_can_do_setop(other)

        if not isinstance(other, PeriodIndex):
            raise ValueError('can only call with other PeriodIndex-ed objects')

        if self.freq != other.freq:
            msg = DIFFERENT_FREQ.format(cls=type(self).__name__,
                                        own_freq=self.freqstr,
                                        other_freq=other.freqstr)
            raise IncompatibleFrequency(msg)
