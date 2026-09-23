    @property
    def _box_func(self):
        """Maybe box an ordinal or Period"""
        # TODO(DatetimeArray): Avoid double-boxing
        # PeriodArray takes care of boxing already, so we need to check
        # whether we're given an ordinal or a Period. It seems like some
        # places outside of indexes/period.py are calling this _box_func,
        # but passing data that's already boxed.
        def func(x):
            if isinstance(x, Period) or x is NaT:
                return x
            else:
                return Period._from_ordinal(ordinal=x, freq=self.freq)

        return func
