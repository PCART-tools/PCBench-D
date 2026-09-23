    def _shallow_copy(self, values=None, freq=None, **kwargs):
        if freq is None:
            freq = self.freq
        if values is None:
            values = self._ndarray_values
        return super(PeriodIndex, self)._shallow_copy(values=values,
                                                      freq=freq, **kwargs)
