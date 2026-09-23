    @freq.setter
    def freq(self, value):
        msg = ('Setting PeriodIndex.freq has been deprecated and will be '
               'removed in a future version; use PeriodIndex.asfreq instead. '
               'The PeriodIndex.freq setter is not guaranteed to work.')
        warnings.warn(msg, FutureWarning, stacklevel=2)
        self._freq = value
