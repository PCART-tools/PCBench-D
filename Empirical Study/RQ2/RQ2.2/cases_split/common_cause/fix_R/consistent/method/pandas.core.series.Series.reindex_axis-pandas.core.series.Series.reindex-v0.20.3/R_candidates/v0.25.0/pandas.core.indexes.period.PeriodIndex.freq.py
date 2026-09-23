    @freq.setter
    def freq(self, value):
        value = Period._maybe_convert_freq(value)
        # TODO: When this deprecation is enforced, PeriodIndex.freq can
        # be removed entirely, and we'll just inherit.
        msg = (
            "Setting {cls}.freq has been deprecated and will be "
            "removed in a future version; use {cls}.asfreq instead. "
            "The {cls}.freq setter is not guaranteed to work."
        )
        warnings.warn(msg.format(cls=type(self).__name__), FutureWarning, stacklevel=2)
        # PeriodArray._freq isn't actually mutable. We set the private _freq
        # here, but people shouldn't be doing this anyway.
        self._data._freq = value
